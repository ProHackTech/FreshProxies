# store proxy information
proxy_ips, proxy_ports = [], []

# change if you don't want to pass arguments all the time
arg_type = '' # proxy type
arg_anonymity = '' # anonymity type
arg_country = '' # country code
arg_filename = '' # custom filename for proxy type
arg_limit = 500 # limit of proxies to save
arg_proxyurl = '' # url for proxy browser or for checking proxies against
arg_pb_timesec = 1000 # timesec to keep browser window alive
arg_maxbrowsers = 10 # maximum browser to open. Default 10
arg_youtubevideo = False # play youtube video
arg_nocheck = False # do not check proxies -> faster
arg_browsermode = 'normal' # 'normal' or 'headless'
arg_threadmode = 'multi' # multi, single, multipool
arg_poolnumber = 5 # pool 5 threads together

# list of abused proxies
abused_proxies = []
