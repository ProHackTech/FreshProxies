import argparse, os, threading, httplib2
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from core.colors import c_white, c_green, c_red, c_yellow, c_blue

'''
_____
TO-DO
-----
+ allow to automatically use proxy browser after grabbing proxy list

+ allow to open specific number of proxy browsers instead of whole list

+ allow proxy grab from other websites

+ allow grabbing specific number of proxies instead of default 26

+ auto check and remove bad proxies

+ migrate to bs4 page search instead of webdriver search

Features will not be developed in order, so keep checking for new versions.

________________________
NOTE ON WEBDRIVER ERRORS
------------------------

- When using proxy browser, you may encounter many webdriver errors. IGNORE THEM.

- These errors occur if a proxy is not working properly. Remove that proxy from the list.

- Feature to check proxies automatically will be made in the future.

'''

# store proxy types
proxy_types = ["HTTP", "HTTPS", "SOCKS4", "SOCKS5"]
# store default file names for "ALL" option
default_output_names = ["proxies_http.txt", "proxies_https.txt", "proxies_socks4.txt", "proxies_socks5.txt"]

# store proxy information
proxy_ips = []
proxy_ports = []

# proxy limit number
number_proxy_limit = 0

# function to save the list
def save_list(output):

	# remove olf file with same filename
	os.remove(output) if os.path.isfile(output) else None

	# open file handler
	print(f"{c_green}[saving list]{c_white}")
	with open(output, 'a') as f:
		# for x in range 0 to length of list of ip's
		for x in range(0, len(proxy_ips)):
			# form a temporary string
			temp_str = f"{proxy_ips[x]}:{proxy_ports[x]}\n"
			# write to file
			f.write(temp_str)

# download function
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
			print(f"{c_green}[Gathered] >> {c_blue}{tempDataElem_ip}{c_yellow}:{c_blue}{tempDataElem_port}{c_white}")
			# sleep(1) # seconds
		except Exception as e:
			print(f"{c_red} -- EXCEPTION -- \n\n{e}{c_white}")

	# quit driver
	driver.quit()

	# save file function
	save_list(output)

# store threads list
rippers = []

# multithreading for "ALL" option
def threader(url, output, pType):
	thread = threading.Thread(target=download_proxy, args=(url, output, pType))
	rippers.append(thread)
	print(f"{c_green}[Formed Thread] >> {c_yellow}{pType}{c_white}")

# function to manage selections
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
	driver.get("https://www.whatismyip.com/") # default URL to make sure you're proxied

	# keeping the browser window open
	if timesec != 0000:
		sleep(timesec)
	else:
		sleep(9999)

	# quit the driver
	driver.quit()

# session for each proxy in proxy file list
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

def git_version():
	hreq = httplib2.Http()
	response_header,content=hreq.request("https://raw.githubusercontent.com/ProHackTech/pytubedown/master/version.me","GET")
	content = content.decode()
	content = int(content)
	return content

def my_version():
	version_me = 1
	# read current version
	with open("VERSION.txt", "r") as fversion:
		for line in fversion:
			version_me = line
	version_me = int(version_me)
	return version_me

def update_check():
	version_me, content = my_version(), git_version()
	# compare versions
	if version_me < content:
		print(f"{c_green}[New Version Available]{c_yellow}There is a new version available!{c_white}\nRun {c_blue}updater.py{c_white} for updating!")
	else:
		print(f"{c_green}[Running Latest]{c_white}")

parser = argparse.ArgumentParser(description="Get Fresh Proxies")
parser.add_argument("-t", "--type", help="Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]", type=str)
parser.add_argument("-f", "--filename", help="Enter Filename [EX: proxies.txt]", type=str)
parser.add_argument("-ts", "--timesec", help="Specify time delay in seconds", type=int)
parser.add_argument("-pb", "--proxybrowser", help="Opens clean browser for proxy list", action="store_true")
parser.add_argument("-upd", "--update", help="Update FreshProxy", action="store_true")

args = parser.parse_args()

if args.type: # grabbing proxies
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
elif args.update:
	update_check()