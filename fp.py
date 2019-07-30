import os, threading, argparse, requests, time
import urllib.request, urllib.error, socket
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from core.colors import c_white, c_green, c_red, c_yellow, c_blue

# store proxy information
proxy_ips, proxy_ports = [], []

# global variable with default values
# change if you don't want to pass arguments all the time, couch potatoe
arg_type = ''
arg_anonymity = ''
arg_country = ''
arg_filename = ''
arg_limit = 500
arg_proxyurl = ''
#arg_randomagent = False
arg_pb_timesec = 1000
arg_maxbrowsers = 10
arg_nocheck = False

# clear screen
def ClrScrn():
	os.system('cls' if os.name == 'nt' else 'clear')

# proxy browser session
def proxy_browser(proxy):
	global arg_pb_timesec
	global arg_proxyurl
	global arg_randomagent
	# apply proxy to firefox using desired capabilities
	PROX = proxy
	webdriver.DesiredCapabilities.FIREFOX['proxy']={
		"httpProxy":PROX,
		"ftpProxy":PROX,
		"sslProxy":PROX,
		"proxyType":"MANUAL"
	}

	#options = Options()
	#options.add_argument("window-size=1400,600")
	driver = webdriver.Firefox()
	# for random user agent
	#if arg_randomagent == True:
	#	from fake_useragent import UserAgent
	#	ua = UserAgent()
	#	options.add_argument(f"user-agent={ua.random}")
	try:
		driver.get(arg_proxyurl)
		# keeping the browser window open
		time.sleep(arg_pb_timesec)
		# close driver
		driver.close()
		driver.quit()
	except Exception as e:
		print(f"{c_red}{e}{c_white}")
		driver.close()
		driver.quit()

# multiple browser threads
# senders :: 0=default | 1=aftergrab
def proxybrowser_ripper(sender):
	global arg_filename
	global arg_maxbrowsers

	# if sender 0, proxies will be taken from saved file
	if sender == 0:
		if arg_filename == '':
			arg_filename = 'proxies.txt'
		# read proxy list
		proxies = [line.rstrip('\n') for line in open(arg_filename)]
	elif sender == 1: # proxies will be taken from list memory
		for x in range(0, len(proxy_ips)):
			proxies  = f"{proxy_ips[x]}:{proxy_ports[x]}"
	# trim to limit
	trimmed_proxies = []
	# set the max browsers limit
	if not arg_maxbrowsers > len(proxies):
		trimmed_proxies = proxies[:arg_maxbrowsers]
	# creating thread list for starting browser thread
	rippers = [threading.Thread(target=proxy_browser, args=(proxy,), daemon=True) for proxy in trimmed_proxies]
	# starting the threads
	for ripper in rippers:
		ripper.start()
	# join the threads to pool
	for ripper in rippers:
		try:
			ripper.join()
		except Exception as e:
			print(f"{c_red}{e}{c_white}")

# Function: Checking proxy response
def proxy_response_check(prox):
	try:
		proxy_handler = urllib.request.ProxyHandler({'http': prox})
		opener = urllib.request.build_opener(proxy_handler)
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib.request.install_opener(opener)
		req=urllib.request.Request(arg_proxyurl)
		sock=urllib.request.urlopen(req)
	except urllib.error.HTTPError as e:
		return e.code
	except Exception as detail:
		return True
	return False

# check dead proxies
def check_dead_proxies():
	global arg_proxyurl
	if arg_proxyurl == '':
		arg_proxyurl = 'https://www.duckduckgo.com/'
	dead_ips, dead_ports = [], []
	socket_timeout = 1
	isAnyDead = False # boolean flag if any dead proxy | small optimization
	print(f"\n\n{c_green}[Checking Dead Proxies]{c_white}")
	print(f"{c_green}[Checking Against] {c_white}>>{c_yellow} {arg_proxyurl}{c_white}")
	# set socket timeout
	print(f"{c_green}[Socket Timeout] {c_white}>>{c_yellow} {socket_timeout}{c_white} seconds")
	socket.setdefaulttimeout(socket_timeout)
	# loop over proxies
	for x in range(0, len(proxy_ips)):
		# generate {proxy:ip}
		prox  = f"{proxy_ips[x]}:{proxy_ports[x]}"
		if proxy_response_check(prox):
			print(f"{c_red}[Dead Proxy] {c_yellow}>>{c_red} {prox}{c_white}")
			isAnyDead = True
			# add dead to lists, because pop messes up indexes while looping
			dead_ips.append(proxy_ips[x])
			dead_ports.append(proxy_ports[x])
		else:
			print(f"{c_green}[Active Proxy] {c_yellow}>>{c_blue} {prox}{c_white}")

	# remove dead proxies
	if isAnyDead == True:
		print(f"\n\n{c_green}[Removing Dead Proxies]{c_white}")
		for x in range(0, len(dead_ips)):
			if dead_ips[x] in proxy_ips[x]:
				print(f"{c_green}[Removing] {c_yellow}>>{c_red} {dead_ips[x]}{c_white}")
				proxy_ips.pop(x)
				proxy_ports.pop(x)

# clean data, bad code..but works
def cleaner_(page_data):
	global arg_filename
	global arg_limit
	global arg_nocheck
	tempfile = "temp.txt"

	# pretty table
	xTable = PrettyTable()
	xTable.field_names = ["Number", "IP Address", "Port"]

	print(f"{c_green}[Cleaning Proxy List]{c_white}")
	# dump to tempfile
	file = open(tempfile,"w")
	file.write(page_data)
	file.close()
	
	# read tempfile
	with open(tempfile) as f:
		content = f.readlines()
	
	# remove tempfile
	try:
		os.remove(tempfile)
	except Exception as e:
		time.sleep(2)
		try:
			os.unlink(tempfile)
		except Exception as ee:
			pass
	
	# clean \r\n
	content = [x.rstrip() for x in content]
	# clean empty index
	content = [item for item in content if item != '']
	
	# add to global list
	for item in content:
		tempprox = item.split(":")
		proxy_ips.append(tempprox[0])
		proxy_ports.append(tempprox[1])
	
	# start auto check
	if not arg_nocheck:
		print(f"{c_white}This will take some time.. Dead proxies will automatically be removed. Relax.")
		check_dead_proxies()
	
	# save clean list
	if arg_filename == '':
		arg_filename = 'proxies.txt'
	f = open(arg_filename,"w")
	num_saved = 0

	# join and write to file
	for x in range(0, arg_limit):
		if not x > (len(proxy_ips)-1):
			joinproxy = f"{proxy_ips[x]}:{proxy_ports[x]}"
			f.write(f"{joinproxy}\n")
			num_saved += 1
			pretty_ip = f"{c_blue}{proxy_ips[x]}{c_white}"
			pretty_port = f"{c_blue}{proxy_ports[x]}{c_white}"
			xTable.add_row([f'{c_yellow}{x}{c_red}', f"{c_blue}{proxy_ips[x]}{c_red}", f"{c_blue}{proxy_ports[x]}{c_red}"])
			#print(xTable)
			#print(f"{c_green}[Proxy:{x}] {c_yellow}>> {c_blue}{proxy_ips[x]}{c_yellow}:{c_blue}{proxy_ports[x]}{c_white}")
	f.close()
	print(xTable)
	print(f"{c_green}[Total Proxies] {c_yellow}>>{c_white} {num_saved}")
	print(f"{c_green}[Save Proxies] {c_yellow}>> {c_blue}{arg_filename}{c_white}")

# selection management
def grabber():
	global arg_type
	global arg_anonymity
	global arg_country
	global arg_filename

	start = time.time()
	arg_type = arg_type.lower()
	proxy_types = ['http', 'https', 'socks4', 'socks5']
	proxy_anonymity = ['transparent', 'anonymous', 'elite']
	url = "https://www.proxy-list.download/api/v1/get?"

	# determining proxy type
	if arg_type == "all":
		for proxy_type in proxy_types:
			url = "https://www.proxy-list.download/api/v1/get?"
			print(f"{c_green}[Proxy Type] {c_yellow}>>{c_yellow} {c_blue}{proxy_type}{c_white}")
			url += f"type={proxy_type}"
			#print(url)
			# determining proxy anonymity
			if not arg_anonymity == '':
				if not arg_anonymity in proxy_anonymity:
					arg_anonymity = "transparent"
					url += f"&anon={arg_anonymity}"
				else:
					url += f"&anon={arg_anonymity}"
				print(f"{c_green}[Anonymity] {c_yellow}>>{c_yellow} {c_blue}{arg_anonymity}{c_white}")
			# determine proxy country
			if not arg_country == '':
				url += f"&country={arg_country}"
				print(f"{c_green}[Country] {c_yellow}>>{c_yellow} {c_blue}{arg_country}{c_white}")
			# get proxies
			try:
				proxies_page = requests.get(url, stream=True)
				arg_filename = f"{proxy_type}.txt"
				page_data = proxies_page.text
				TGrab = threading.Thread(target=cleaner_, args=(page_data,), daemon=True)
				TGrab.start()
				TGrab.join()
			except Exception as e:
				print(f"{c_red}{e}{c_white}")
			print("\n")
	elif arg_type in proxy_types:
		# if bulk flag, run the bulk grabber before default
		url = "https://www.proxy-list.download/api/v1/get?"
		url += f"type={arg_type}"
		print(f"{c_green}[Proxy Type] {c_yellow}>>{c_yellow} {c_blue}{arg_type.upper()}{c_white}")
		# determining proxy anonymity
		if not arg_anonymity == '':
			if not arg_anonymity in proxy_anonymity:
				arg_anonymity = "transparent"
				url += f"&anon={arg_anonymity}"
			else:
				url += f"&anon={arg_anonymity}"
			print(f"{c_green}[Anonymity] {c_yellow}>>{c_yellow} {c_blue}{arg_anonymity}{c_white}")
		# determine proxy country
		if not arg_country == '':
			url += f"&country={arg_country}"
			print(f"{c_green}[Country] {c_yellow}>>{c_yellow} {c_blue}{arg_country}{c_white}")
		# get proxies
		proxies_page = requests.get(url, stream=True)
		#print(proxies_page.text)
		cleaner_(proxies_page.text)
	else:
		# set to default http
		arg_type = "http"
		grabber()

	duration = time.time() - start
	print(f"{c_green}[Time Taken] {c_yellow}>> {c_blue}{duration}{c_white}\n\n")

# read git version
def git_version():
	response = urllib.request.urlopen("https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/VERSION.txt")
	for content in response:
		return int(content)

# read local version
def my_version():
	version_me = 1
	# read current version
	with open("VERSION.txt", "r") as fversion:
		for line in fversion:
			version_me = line
	version_me = int(version_me)
	return version_me

# check update
def update_check():
	version_me, content = my_version(), git_version()
	# compare versions
	if version_me < content:
		print(f"{c_green}[New Version Available]{c_yellow}There is a new version available!{c_white}")
		print(f"{c_yellow}-- Follow These Steps To Update --")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} cd updater {c_white}(To go inside updater directory)")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} python updater.py {c_white}(To run updater)")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} cd ../  {c_white}(To go back into main directory)")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} python fp.py  {c_white}(To run again)\n")
		version_diff = (content - version_me)
		print(f"{c_green}[Running Behind] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")
	elif version_me == content:
		print(f"{c_green}[Running Latest] {c_yellow}>> {c_green}v{c_white}{version_me}\n\n")
	elif version_me > content:
		version_diff = (version_me - content)
		print(f"{c_green}[Running Ahead] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")

def banner():
	ClrScrn()
	print(f'''{c_green}
 _______              _     ______                _            
(_______)            | |   (_____ \              (_)           
 _____ ____ ____  ___| | _  _____) )___ ___ _   _ _  ____  ___ 
|  ___) ___) _  )/___) || \|  ____/ ___) _ ( \ / ) |/ _  )/___)
| |  | |  ( (/ /|___ | | | | |   | |  | |_| ) X (| ( (/ /|___ |
|_|  |_|   \____|___/|_| |_|_|   |_|   \___(_/ \_)_|\____|___/ {c_white}
		''')

	print(f"\n[Version Check]...")
	update_check()

def pretty_help():
	banner()
	hTable = PrettyTable()
	hTable.field_names = [f"{c_yellow}Argument Less", "Argument Full", f"Description{c_white}"]
	hTable.add_row([f'{c_green}-t{c_red}', f'{c_green}--type{c_red}', f'{c_white}Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]'])
	hTable.add_row([f'{c_green}-a{c_red}', f'{c_green}--anonymity{c_red}', f'{c_white}Enter Anonymity Type [transparent/anonymous/elite]'])
	hTable.add_row([f'{c_green}-c{c_red}', f'{c_green}--country{c_red}', f'{c_white}Enter Country ISO Code [US/RU/IN etc..]'])
	hTable.add_row([f'{c_green}-f{c_red}', f'{c_green}--filename{c_red}', f'{c_white}Enter Filename [EX: proxies.txt]'])
	hTable.add_row([f'{c_green}-l{c_red}', f'{c_green}--limit{c_red}', f'{c_white}Enter max proxies to save'])
	hTable.add_row([f'{c_green}-nocheck{c_red}', f'{c_green}--nocheck{c_red}', f'{c_white}Donot check for dead proxies'])
	hTable.add_row([f'{c_green}-pb{c_red}', f'{c_green}--proxybrowser{c_red}', f'{c_white}Opens browser for proxies'])
	hTable.add_row([f'{c_green}-pu{c_red}', f'{c_green}--proxyurl{c_red}', f'{c_white}Enter your custom url for proxy browser'])
	hTable.add_row([f'{c_green}-ts{c_red}', f'{c_green}--timesec{c_red}', f'{c_white}Time seconds to keep browsers alive'])
	hTable.add_row([f'{c_green}-mb{c_red}', f'{c_green}--maxbrowsers{c_red}', f'{c_white}Maximum number of browsers to open'])
	print(hTable)

def init():
	# global args variable
	global arg_type
	global arg_anonymity
	global arg_country
	global arg_filename
	global arg_checkdead
	global arg_limit
	global arg_proxyurl
	#global arg_randomagent
	global arg_pb_timesec
	global arg_maxbrowsers
	global arg_nocheck

	banner()
	parser = argparse.ArgumentParser(description="FreshProxies", add_help=False)
	parser.add_argument("-h", "--help", help="Help Menu", action="store_true")

	# filters for gathering proxies
	parser.add_argument("-t", "--type", type=str)
	parser.add_argument("-a", "--anonymity", type=str)
	parser.add_argument("-c", "--country", type=str)
	parser.add_argument("-f", "--filename", type=str)
	parser.add_argument("-l", "--limit", type=int)

	# don't check for dead proxies
	parser.add_argument("-nocheck", "--nocheck", action="store_true")

	# proxy browser options
	parser.add_argument("-pb", "--proxybrowser", action="store_true")
	parser.add_argument("-pu", "--proxyurl", type=str)
	#parser.add_argument("-ra", "--randomagent", action="store_true")
	parser.add_argument("-ts", "--timesec", type=int)
	parser.add_argument("-mb", "--maxbrowsers", type=int)

	args = parser.parse_args()

	# if help
	if args.help:
		pretty_help()
		exit()

	# settings the global vars
	if args.anonymity:
		arg_anonymity = args.anonymity
	if args.country:
		arg_country = args.country
	if args.filename:
		arg_filename = args.filename
	if args.limit:
		arg_limit = args.limit
	if args.proxyurl:
		arg_proxyurl = args.proxyurl
	#if args.randomagent:
	#	arg_randomagent = True
	if args.timesec:
		arg_pb_timesec = args.timesec
	if args.maxbrowsers:
		arg_maxbrowsers = args.maxbrowsers
	if args.nocheck:
		arg_nocheck = True

	if args.type:
		arg_type = args.type
		grabber()
		if args.proxybrowser:
			proxybrowser_ripper(1)
	elif args.proxybrowser:
		proxybrowser_ripper(0)

if __name__ == "__main__":
	init()
