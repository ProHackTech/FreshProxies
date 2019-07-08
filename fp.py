import argparse, os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

'''

Developed by: Bhavesh Kaul | ProHack.Tech
@ 2019

-- What is this? --
[+] Small script to download fresh proxy lists with {ip:port} format.
[+] Get HTTP, HTTPS, SOCKS4, SOCKS5 proxies, or all.

Show some love and star on GitHub.

_____
TO-DO
-----
+ allow users to decide number of proxies to download
+ add support from other website

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
	with open(output, 'a') as f:
		# for x in range 0 to length of list of ip's
		for x in range(0, len(proxy_ips)):
			# form a temporary string
			temp_str = f"{proxy_ips[x]}:{proxy_ports[x]}\n"
			# write to file
			f.write(temp_str)

# download function - important boi
def download_proxy(url, output):
	
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
		temp_xpath_ip = f"/html/body/div/main/div/div[3]/div/table/tbody/tr[{x}]/td[1]"
		temp_xpath_port = f"/html/body/div/main/div/div[3]/div/table/tbody/tr[{x}]/td[2]"
		try:
			tempDataElem_ip = driver.find_element_by_xpath(temp_xpath_ip).text
			tempDataElem_port = driver.find_element_by_xpath(temp_xpath_port).text
			proxy_ips.append(tempDataElem_ip)
			proxy_ports.append(tempDataElem_port)
			print(f"Gathered IP:PORT >> {tempDataElem_ip}:{tempDataElem_port}")
			# remove this comment if there is ElementNotFound errors
			# but this will make it 200% slower to gather ip's -\(+_+)/-
			# sleep(1) # seconds
		except Exception as e:
			pass

	# quit driver
	driver.quit()

	# save file function
	save_list(output)

# function to manage selections
# made it to seperate selections from download function
# i find it cleaner this way
def selection_manager(pType, output):
	# define constant url
	url = "https://www.proxy-list.download/"

	# make pType lower() to reduce code
	pType = pType.lower()

	if pType == "all": # if proxy type selection is 'ALL'
		for x in range(0, len(proxy_types)): # if 'x' is in range from index 0 to length of proxy_types list
			url = f"{url}{proxy_types[x]}" # generate url string to pass in download function
			download_proxy(url, default_output_names[x]) # run download function for each loop with default names
	else: # if proxy type is anything other than 'ALL'
		url = f"{url}{pType.upper()}"
		download_proxy(url, output)


parser = argparse.ArgumentParser(description="Get Fresh Proxies")
parser.add_argument("-t", "--type", help="Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]", type=str)
parser.add_argument("-n", "-number", help="Enter the number of proxies you want [DEFAULT: 10]", type=int)
parser.add_argument("-o", "--output", help="Enter Filename [EX: proxies.txt]", type=str)
args = parser.parse_args()

if args.number:
	number_proxy_limit = args.number
else:
	number_proxy_limit = 10
if args.type:
	if args.output:
		selection_manager(args.type, args.output)
	else:
		selection_manager(args.type, "proxies.txt")