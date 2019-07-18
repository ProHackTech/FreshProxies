import os, threading, argparse
import urllib.request, urllib.error, socket
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from core.colors import c_white, c_green, c_red, c_yellow, c_blue

'''
________________
WHAT'S NEW v1003
----------------

+ Fix global variable set issue
+ Fix proxy browser after grab bug
+ User can add custom url for proxy browser

_____
TO-DO
-----
+ optimize element searching on webdriver

+ allow to open specific number of proxy browsers instead of whole list

+ allow proxy grab from other websites

+ allow grabbing specific number of proxies instead of default 26

+ migrate to bs4 page search instead of webdriver search

+ auto update check on start (but not run updater)

Features will not be developed in order, so keep checking for new versions.

________________________
NOTE ON WEBDRIVER ERRORS
------------------------

- When using proxy browser, you may encounter many webdriver errors. IGNORE THEM.

- These errors occur if a proxy is not working properly. Remove that proxy from the list.

- use --checkdead flag to auto check and remove dead proxies 

'''

# store proxy types
proxy_types = ["HTTP", "HTTPS", "SOCKS4", "SOCKS5"]
# store default file names for "ALL" option
default_output_names = ["proxies_http.txt", "proxies_https.txt", "proxies_socks4.txt", "proxies_socks5.txt"]

# store proxy information
proxy_ips, proxy_ports = [], []

# for storing if checkdead flag is passed, false by default
CheckDeadProxies = False
# for proxybrowser with proxy grab, false by default
ProxifyAfterGrab = False
ProxifyAfterGrab_TimeSec = 0000
# url for proxy browser
proxify_url = ''

# Function: Clearing screen.. no hate pls. I need quick fixes
def ClrScrn():
	os.system('cls' if os.name == 'nt' else 'clear')

# Function: To save the list
def save_list(output):
	# remove olf file with same filename
	os.remove(output) if os.path.isfile(output) else None

	# open file handler
	print(f"{c_yellow}[saving list]{c_white}")
	with open(output, 'a') as f:
		# for x in range 0 to length of list of ip's
		for x in range(0, len(proxy_ips)):
			# form a temporary string
			temp_str = f"{proxy_ips[x]}:{proxy_ports[x]}\n"
			# write to file
			f.write(temp_str)
	print(f"{c_green}[Saved] >> {c_blue}{output}{c_white}")

# Function: Ping to check availability
''' 
Not used because proxies do not respond to PING
So using urlopen instead to check

def pinger(host):
	Import platform, subprocess
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True
    # return boolean
    return subprocess.call(args, shell=need_sh) == 0
'''

# Function: To start proxies Firefox session
def proxify_start(proxy, timesec):
	# apply proxy to firefox
	PROX = proxy
	webdriver.DesiredCapabilities.FIREFOX['proxy']={
		"httpProxy":PROX,
		"ftpProxy":PROX,
		"sslProxy":PROX,
		"proxyType":"MANUAL"
	}

	# start webdriver
	driver = webdriver.Firefox()
	### ENTER YOUR CUSTOM URL HERE v
	driver.get(proxify_url) # default URL to make sure you're proxied

	# keeping the browser window open
	if timesec != 0000:
		sleep(timesec)
	else:
		sleep(9999)

	# quit the driver
	driver.quit()

# Function: Session for each proxy in proxy file list
def proxify_session(filename, timesec):
	# read proxy list
	proxies = [line.rstrip('\n') for line in open(filename)]

	# creating thread list for starting browser thread
	rippers = [threading.Thread(target=proxify_start, args=(proxy,timesec)) for proxy in proxies]

	# starting the threads
	for ripper in rippers:
		ripper.start()
	# join the threads to pool
	for ripper in rippers:
		ripper.join()

# Function: Checking proxy response
def proxy_response_check(prox):    
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': prox})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('https://www.google.com')
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        #print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        #print("ERROR:", detail)
        return True
    return False

# Function: To check and remove dead proxies
def check_dead_proxies():
	dead_ips, dead_ports = [], []
	socket_timeout = 5
	isAnyDead = False # boolean flag if any dead proxy | small optimization
	print(f"\n\n{c_green}[Checking Dead Proxies]{c_white}")
	print(f"{c_green}[Checking Against] {c_white}>>{c_yellow} https://www.google.com/{c_white}")
	# set socket timeout
	print(f"{c_green}[Socket Timeout] {c_white}>>{c_yellow} {socket_timeout}{c_white}")
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

# Function: To gather the proxies
def download_proxy(url, output, pType):
	# clean lists for 'ALL' option
	proxy_ips.clear()
	proxy_ports.clear()
	
	# initialize web driver
	options = Options()
	options.headless = True # headless mode
	driver = webdriver.Firefox(options=options)
	driver.get(url)

	# perform page scroll to end of body
	driver.find_element_by_tag_name('body').send_keys(Keys.END)
	sleep(1)

	# get number of table rows on page
	numTR = driver.find_elements_by_xpath("//tr")

	# get information
	for x in range(1, len(numTR)):
		# if http proxy, then 2nd last div is 3, else 2
		if pType == "http":
			temp_xpath_ip = f"/html/body/div/main/div/div[3]/div/table/tbody/tr[{x}]/td[1]"
			temp_xpath_port = f"/html/body/div/main/div/div[3]/div/table/tbody/tr[{x}]/td[2]"
		else:
			temp_xpath_ip = f"/html/body/div/main/div/div[2]/div/table/tbody/tr[{x}]/td[1]"
			temp_xpath_port = f"/html/body/div/main/div/div[2]/div/table/tbody/tr[{x}]/td[2]"
		# get the elements
		try:
			tempDataElem_ip = driver.find_element_by_xpath(temp_xpath_ip).text
			tempDataElem_port = driver.find_element_by_xpath(temp_xpath_port).text
			proxy_ips.append(tempDataElem_ip)
			proxy_ports.append(tempDataElem_port)
			print(f"{c_green}[Gathered] {c_yellow}>> {c_blue}{tempDataElem_ip}{c_yellow}:{c_blue}{tempDataElem_port}{c_white}")
			# sleep(1) # seconds
		except Exception as e:
			print(f"{c_red} -- EXCEPTION -- \n\n{e}{c_white}")

	# quit driver
	driver.quit()

	# if checkdead flag passed
	if CheckDeadProxies:
		check_dead_proxies()

	# save proxies to file
	save_list(output)

	# proxify browser after grab
	if ProxifyAfterGrab:
		proxify_session(output, ProxifyAfterGrab_TimeSec)

# store threads list
rippers = []

# Function: Multithreading for "ALL" option
def threader(url, output, pType):
	thread = threading.Thread(target=download_proxy, args=(url, output, pType))
	rippers.append(thread)
	print(f"{c_green}[Formed Thread] >> {c_yellow}{pType}{c_white}")

# Function: To manage selections
def selection_manager(pType, output):
	# define constant url
	url = "https://www.proxy-list.download/"

	# make pType lower() to reduce code
	pType = pType.lower()

	if pType == "all": # if proxy type selection is 'ALL'
		#print(f"Fixing multithreading bug for [ALL] option. Please use seperate options or now :/")
		
		for x in range(0, len(proxy_types)): # if 'x' is in range from index 0 to length of proxy_types list
			print(f"{c_green}[Proxy Type] {c_yellow}>>{c_yellow} {c_blue}{proxy_types[x]}{c_white}")
			url = "https://www.proxy-list.download/" # clean the url, or else it appends for each loop
			url = f"{url}{proxy_types[x]}" # generate url string to pass in download function
			print(f"{c_green}[URL] {c_yellow}>>{c_yellow} {c_white}{url}")
			threader(url, default_output_names[x], pType) # run download function for each loop with default names
		for ripper in rippers:
			print(f"{c_green}[Starting Thread] >> {c_yellow}{ripper}{c_white}")
			ripper.start()
			print(f"{c_green}[Joining Thread] >> {c_yellow}{ripper}{c_white}")
			ripper.join()
		#for ripper in rippers:
		#	print(f"{c_green}[Joining Thread] >> {c_yellow}{ripper}{c_white}")
		#	ripper.join()
		
	else: # if proxy type is anything other than 'ALL'
		url = f"{url}{pType.upper()}"
		download_proxy(url, output, pType)

# Function: Read VERSION.txt on GitHub
def git_version():
	response = urllib.request.urlopen("https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/VERSION.txt")
	for content in response:
		return int(content)

# Function: Read local VERSION.txt file
def my_version():
	version_me = 1
	# read current version
	with open("VERSION.txt", "r") as fversion:
		for line in fversion:
			version_me = line
	version_me = int(version_me)
	return version_me

# Function: To compare GitHub and Local version numbers
def update_check():
	version_me, content = my_version(), git_version()
	# compare versions
	if version_me < content:
		print(f"{c_green}[New Version Available]{c_yellow}There is a new version available!{c_white}\nRun {c_blue}/updater/update.py{c_white} for updating!")
		version_diff = (content - version_me)
		print(f"{c_green}[Running Behind] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")
	elif version_me == content:
		print(f"{c_green}[Running Latest] {c_yellow}>> {c_green}v{c_white}{version_me}\n\n")
	elif version_me > content:
		version_diff = (version_me - content)
		print(f"{c_green}[Running Ahead] {c_yellow}>> {c_green}{version_diff} {c_white}versions\n\n")

def banner():
	ClrScrn()
	print(f'''{c_blue}
 _______              _     ______                _            
(_______)            | |   (_____ \              (_)           
 _____ ____ ____  ___| | _  _____) )___ ___ _   _ _  ____  ___ 
|  ___) ___) _  )/___) || \|  ____/ ___) _ ( \ / ) |/ _  )/___)
| |  | |  ( (/ /|___ | | | | |   | |  | |_| ) X (| ( (/ /|___ |
|_|  |_|   \____|___/|_| |_|_|   |_|   \___(_/ \_)_|\____|___/ {c_white}
		''')

	print(f"\n[Version Check]...")
	update_check()

# Function: Initialize script
def init():
	# global variables
	global CheckDeadProxies
	global ProxifyAfterGrab
	global ProxifyAfterGrab_TimeSec
	global proxify_url

	# FreshProxies banner
	banner()
	# argument parsing
	parser = argparse.ArgumentParser(description="FreshProxies")
	# proxy type to gather
	parser.add_argument("-t", "--type", help="Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]", type=str)
	# enter a filename
	parser.add_argument("-f", "--filename", help="Enter Filename [EX: proxies.txt]", type=str)
	# check and remove dead proxies
	parser.add_argument("-checkd", "--checkdead", help="Check and remove dead proxies", action="store_true")
	# enter time in seconds
	parser.add_argument("-ts", "--timesec", help="Specify time delay in seconds", type=int)
	# proxy browser mode
	parser.add_argument("-pb", "--proxybrowser", help="Opens clean browser for proxy list", action="store_true")
	# proxy url for proxy browser
	parser.add_argument("-pu", "--proxyurl", help="Enter your custom url for proxy browser", type=str)
	# update freshproxy
	parser.add_argument("-upd", "--update", help="Update FreshProxy", action="store_true")

	args = parser.parse_args()

	if args.type: # grabbing proxies
		# if checkdead flag is set
		if args.checkdead:
			CheckDeadProxies = True
		# if proxybrowser flag is set
		if args.proxybrowser: # proxify after grab
			ProxifyAfterGrab = True
			# if timesec is specified
			if args.timesec:
				ProxifyAfterGrab_TimeSec = args.timesec
			# if proxy url specified:
			if args.proxyurl:
				proxify_url = args.proxyurl
			else:
				proxify_url = "https://www.whatismyip.com/"
		# if filename is specified
		if args.filename:
			selection_manager(args.type, args.filename)
		else:
			selection_manager(args.type, "proxies.txt")
	elif args.proxybrowser: # proxy browser
		if args.filename:
			if args.timesec:
				proxify_session(filename, args.timesec)
			else:
				proxify_session(filename, 0000)
		else:
			if args.timesec:
				proxify_session("proxies.txt", args.timesec)
			else:
				proxify_session("proxies.txt", 0000)
	elif args.update: # checking for updates
		update_check()

# main
if __name__ == "__main__":
	init()
