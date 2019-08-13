import os, threading, argparse, requests, time
import urllib.request, urllib.error, socket, shutil
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from core.colors import c_white, c_green, c_red, c_yellow, c_blue
from core.config import *

# clear screen
def ClrScrn():
	os.system('cls' if os.name == 'nt' else 'clear')

# proxy browser session
def proxy_browser(proxy):
	global arg_pb_timesec
	global arg_proxyurl
	global arg_youtubevideo
	global arg_browsermode

	# recheck proxyurl
	if arg_proxyurl == '':
		arg_proxyurl = 'https://www.duckduckgo.com/'
	# apply proxy to firefox using desired capabilities
	PROX = proxy
	webdriver.DesiredCapabilities.FIREFOX['proxy']={
		"httpProxy":PROX,
		"ftpProxy":PROX,
		"sslProxy":PROX,
		"proxyType":"MANUAL"
	}

	options = Options()
	# for browser mode
	options.headless = False
	if arg_browsermode == 'headless':
		options.headless = True
	driver = webdriver.Firefox(options=options)
	try:
		print(f"{c_green}[URL] >> {c_blue}{arg_proxyurl}{c_white}")
		print(f"{c_green}[Proxy Used] >> {c_blue}{proxy}{c_white}")
		print(f"{c_green}[Browser Mode] >> {c_blue}{arg_browsermode}{c_white}")
		print(f"{c_green}[TimeSec] >> {c_blue}{arg_pb_timesec}{c_white}\n\n")
		
		driver.get(arg_proxyurl)
		time.sleep(2) # seconds
		# check if redirected to google captcha (for quitting abused proxies)
		if not "google.com/sorry/" in driver.current_url:
			# if youtube view mode
			if arg_youtubevideo:
				delay_time = 5 # seconds
				# if delay time is more than timesec for proxybrowser
				if delay_time > arg_pb_timesec:
					# increase proxybrowser timesec
					arg_pb_timesec += 5
					# wait for the web element to load
					try:
						player_elem = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.ID, 'movie_player')))
						togglebtn_elem = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.ID, 'toggleButton')))
						time.sleep(2)
						# click player
						webdriver.ActionChains(driver).move_to_element(player_elem).click(player_elem).perform()
						try:
							# click autoplay button to disable autoplay
							webdriver.ActionChains(driver).move_to_element(togglebtn_elem).click(togglebtn_elem).perform()
						except Exception:
							pass
					except TimeoutException:
						print("Loading video control took too much time!")
		else:
			print(f"{c_red}[Network Error] >> Abused Proxy: {proxy}{c_white}")
			driver.close()
			driver.quit()
			if proxy not in abused_proxies:
				abused_proxies.append(proxy)
	except Exception as e:
		print(f"{c_red}{e}{c_white}")
		driver.close()
		driver.quit()

# Yield successive n-sized chunks from rippers list
def multipool_chunks(rippers):
	global arg_poolnumber
	global arg_maxbrowsers

	# if pool number is not less than or equal to 0
	if not arg_poolnumber <= 0:
		# if pool number is not more than or equal to max browsers
		if not arg_poolnumber >= arg_maxbrowsers:
			# yeild the chunks
			for i in range(0, len(rippers), arg_poolnumber):
				yield rippers[i:i + arg_poolnumber]
		else:
			# print error and exit the script
			print(f"{c_red}[MultiPool Error] >> {c_yellow}(poolnumber){c_red} can not greater than{c_yellow} (maxbrowser number){c_white}")
			exit()

# chunk runner
def browser_chunk_ripper(chunk_list):
	# chunk_list will act like 'rippers' threads list as in multi option
	for chunk_thread in chunk_list:
		chunk_thread.start()
	for chunk_thread in chunk_list:
		try:
			chunk_thread.join()
			print(f"{c_green}[Thread] >> {c_yellow}Number:{c_blue}{chunk_thread}{c_white}")
		except Exception as e:
			print(f"{c_red}{e}{c_white}")

# multiple browser threads
# senders :: 0=default | 1=aftergrab
def proxybrowser_ripper(sender):
	global arg_filename
	global arg_maxbrowsers
	global arg_threadmode
	global arg_poolnumber

	# if thread mode is empty, set as multi
	if arg_threadmode == '':
		arg_threadmode = 'multi'

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
	# thread mode
	if arg_threadmode == 'multi':
		print(f"{c_green} -- [Multi Mode] --{c_white}\n")
		# starting threads
		for ripper in rippers:
			ripper.start()
		# join all threads at once (multi)
		for ripper in rippers:
			try:
				ripper.join()
				print(f"{c_green}[Thread] >> {c_yellow}Number:{c_blue}{ripper}{c_white}")
			except Exception as e:
				print(f"{c_red}{e}{c_white}")
	elif arg_threadmode == 'single':
		print(f"{c_green} -- [Single Mode] --{c_white}\n")
		# starting and joining the thread one by one (single)
		for ripper in rippers:
			try:
				ripper.start()
				ripper.join()
				print(f"{c_green}[Thread Joined] >> {c_yellow}Number:{c_blue}{ripper}{c_white}")
			except Exception as e:
				print(f"{c_red}{e}{c_white}")
	elif arg_threadmode == 'multipool':
		print(f"{c_green} -- [Multi-Pool Mode] --{c_white}\n")
		print(f"{c_green}[Pools/Chunks] >> {c_yellow}of Number: {c_blue}{arg_poolnumber}{c_white}")
		# yield chunks for threads
		chunks_list = multipool_chunks(rippers)
		# for each list of chunks
		for each_chunk in chunks_list:
			browser_chunk_ripper(each_chunk)
			time.sleep(5)

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
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} python update.py {c_white}(To run updater)")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} cd ../  {c_white}(To go back into main directory)")
		print(f"{c_green}[Type] {c_yellow}>>{c_blue} python fp.py  {c_white}(To run again)\n")
		version_diff = (content - version_me)
		print(f"{c_green}[Running Behind] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")
	elif version_me == content:
		print(f"{c_green}[Running Latest] {c_yellow}>> {c_green}v{c_white}{version_me}\n\n")
	elif version_me > content:
		version_diff = (version_me - content)
		print(f"{c_green}[Running Ahead] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")

# updater update
def updater_update():
	filename = "update.py"
	filepath = f"updater/{filename}"
	if os.path.isfile(filename):
		os.remove(filename)
	try:
		urllib.request.urlretrieve("https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/updater/update.py", filename)
		if os.path.isfile(filepath):
			os.remove(filepath)
		shutil.move(filename, filepath)
	except Exception as e:
		print(f"{c_red}[Error] >> Unable to download {c_blue}update.py{c_red}\n\n{e}\n\nEXITING!{c_white}")
		exit()

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
	updater_update()

def pretty_help():
	ClrScrn()
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
	hTable.add_row([f'{c_green}-bm{c_red}', f'{c_green}--browsermode{c_red}', f'{c_white}"normal" or "headless" browser window'])
	hTable.add_row([f'{c_green}-tm{c_red}', f'{c_green}--threadmode{c_red}', f'{c_white}"multi" or "single" or "multipool"'])
	hTable.add_row([f'{c_green}-pn{c_red}', f'{c_green}--poolnumber{c_red}', f'{c_white}Enter a number of browsers to pool for multipool option'])
	hTable.add_row([f'{c_green}-ytv{c_red}', f'{c_green}--ytvideo{c_red}', f'{c_white}Play YouTube video (for view botting)'])
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
	global arg_pb_timesec
	global arg_maxbrowsers
	global arg_youtubevideo
	global arg_nocheck
	global arg_browsermode
	global arg_threadmode
	global arg_poolnumber

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
	parser.add_argument("-ts", "--timesec", type=int)
	parser.add_argument("-mb", "--maxbrowsers", type=int)
	parser.add_argument("-bm", "--browsermode", type=str)
	parser.add_argument("-tm", "--threadmode", type=str)
	parser.add_argument("-pn", "--poolnumber", type=int)
	parser.add_argument("-ytv", "--ytvideo", action="store_true")

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
	if args.timesec:
		arg_pb_timesec = args.timesec
	if args.maxbrowsers:
		arg_maxbrowsers = args.maxbrowsers
	if args.ytvideo:
		arg_youtubevideo = True
	if args.nocheck:
		arg_nocheck = True
	if args.browsermode:
		arg_browsermode = args.browsermode
	if args.threadmode:
		arg_threadmode = args.threadmode
	if args.poolnumber:
		arg_poolnumber = args.poolnumber

	if args.type:
		arg_type = args.type
		grabber()
		if args.proxybrowser:
			proxybrowser_ripper(1)
	elif args.proxybrowser:
		proxybrowser_ripper(0)

if __name__ == "__main__":
	init()
