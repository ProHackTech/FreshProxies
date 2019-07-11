import argparse, os, threading
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from core.colors import c_white, c_green, c_red, c_yellow, c_blue

'''
_____
TO-DO
-----
+ allow users to decide number of proxies to download
+ add support from other proxy lists

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


parser = argparse.ArgumentParser(description="Get Fresh Proxies")
parser.add_argument("-t", "--type", help="Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]", type=str)
parser.add_argument("-o", "--output", help="Enter Filename [EX: proxies.txt]", type=str)
args = parser.parse_args()

if args.type:
	if args.output:
		selection_manager(args.type, args.output)
	else:
		selection_manager(args.type, "proxies.txt")