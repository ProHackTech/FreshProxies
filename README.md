<h1 align="center">
	<br>
	<img src="https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/git_assets/logo.png" alt="FreshProxy Logo">
	<br>
	FreshProxies
</h1>

Python script to grab HTTP, HTTPS, SOCKS4 and SOCKS5 proxies fast. Open multiple proxied browsers.

## Instructions

You need the following python packages installed: argparse, selenium, requests, ptable

You can install all by:

### Windows 

> python3 -m pip install -r requirements.txt

### Linux

> pip3 install -r requirements.txt

or

> python3-pip install -r requirements.txt

You will need Firefox installed on the system. Gecko driver executable file is provieded for Windows users. Linux users can enjoy without any executables, as long as Firefox is installed.

## Features

- [x] Grab Http/Https/Socks4/Socks5 proxies
- [x] Specify number of proxies to save
- [x] Filter proxies by country
- [x] Filter proxies by anonymity
- [x] Open proxied Firefox instances for proxies in file list
- [x] Open proxied Firefox instances after grabbing proxy list
- [x] Check against URL and remove dead proxies automatically (optional)
- [x] Specify time to keep proxied browsers active
- [x] Specify custom url for proxy browsers
- [x] FreshProxies auto-update-check

### Whats New [v1007]

- [x] Added pretty table
- [x] Fix 'all' options 404 Error
- [x] Better help menu (argparse help is ugly af)

*Note:* For some weird reason, proxy browser after grab is making the proxy servers refuse connections :< idk wth is wrong with this shitz. But regular command without grab works fine..

## How To

### Video Demonstration (old version)

*Grabbing Proxies*

<h3 align="center">
	<a href="https://www.youtube.com/watch?v=PlC5wXNXg1A" target="_blank">
		<img src="http://img.youtube.com/vi/PlC5wXNXg1A/0.jpg" alt="FreshProxy Demo" width="480" height="360" border="10" />
	</a>
</h3>

### HTTP Proxy

> python fp.py --type http

### HTTPS Proxy

> python fp.py -t https

### SOCKS4 Proxy

> python fp.py -t socks4

### SOCKS5 Proxy

> python fp.py -t socks5

### ALL Proxies

> python fp.py -t all

## Proxify Browser

This option allows you to open multi-threaded instances of Firefox run through proxies in the proxy list.

### Arguments available to use

*-pb* : proxy browser

*-pu* : custom url

*-mb* : maximum browsers to open

*-ts* : timesec to run the browser sessions

*-f* : specify the proxy file list

### Proxify using default list

Uses default proxy list with name "proxies.txt"

> python fp.py -pb

### Proxify using custom list

> python fp.py -pb -f your_proxy_list.txt

### Proxify using custom list and timesec (quick automation)

> python fp.py -pb -f proxies.txt -ts 120

### Proxify with timesec and default proxy list

> python fp.py -pb -ts 120

### Proxifies browser with custom url

> python fp.py -pb -pu "https://your_url.something/"

## Proxy Browser after proxy grab

All proxy browser commands available here

## Example

The following command will perform these actions:

 - grab http proxies (-t)

 - do not check for dead proxies (--nocheck)

 - save only 50 proxies (-l)

 - start 10 proxied browsers, with your url for 240 seconds

> python fp.py -t http -nocheck -l 50 -pb -pu "https://your_website.com/" -ts 240 -mb 10


**More arguments can be found using --help menu**

## License

```

MIT License

Copyright (c) 2019 prohack.tech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
