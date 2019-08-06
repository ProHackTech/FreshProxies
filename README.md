<h1 align="center">
	<br>
	<img src="https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/git_assets/logo.png" alt="FreshProxy Logo">
	<br>
	FreshProxies
</h1>

Python script to grab HTTP, HTTPS, SOCKS4 and SOCKS5 proxies fast. Open multiple proxied browsers. Get unique views.

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
- [x] Specify maximum proxy browsers to open
- [x] Browsers in normal or headless mode
- [x] Youtube mode - auto play videos once player element is loaded (for view bot)
- [x] FreshProxies auto-update-check

### Whats New [v1009]

- [x] Add browser mode 'normal' or 'headless'
- [x] Add verbosity to proxy browser threads

*Note:* For some weird reason, proxy browser after grab is making the proxy servers refuse connections :< But regular command without grab works fine..

## How To

### Video Demonstration (old version!!)

*Grabbing Proxies*

<h3 align="center">
	<a href="https://www.youtube.com/watch?v=PlC5wXNXg1A" target="_blank">
		<img src="http://img.youtube.com/vi/PlC5wXNXg1A/0.jpg" alt="FreshProxy Demo" width="480" height="360" border="10" />
	</a>
</h3>

### Help Menu
Can be accessed using '-h' or '--help'

'''
+---------------+----------------+----------------------------------------------------+
| Argument Less | Argument Full  |                    Description                     |
+---------------+----------------+----------------------------------------------------+
|       -t      |     --type     |  Enter Proxy Type [HTTP/HTTPS/SOCKS4/SOCKS5/ALL]   |
|       -a      |  --anonymity   | Enter Anonymity Type [transparent/anonymous/elite] |
|       -c      |   --country    |      Enter Country ISO Code [US/RU/IN etc..]       |
|       -f      |   --filename   |          Enter Filename [EX: proxies.txt]          |
|       -l      |    --limit     |             Enter max proxies to save              |
|    -nocheck   |   --nocheck    |            Donot check for dead proxies            |
|      -pb      | --proxybrowser |             Opens browser for proxies              |
|      -pu      |   --proxyurl   |      Enter your custom url for proxy browser       |
|      -ts      |   --timesec    |        Time seconds to keep browsers alive         |
|      -mb      | --maxbrowsers  |         Maximum number of browsers to open         |
|      -bm      | --browsermode  |       "normal" or "headless" browser window        |
|      -ytv     |   --ytvideo    |       Play YouTube video (for view botting)        |
+---------------+----------------+----------------------------------------------------+
'''


## Example Command (proxy browser)

The following command will perform these actions:

 - start 5 proxied browsers, with your url for 240 seconds

 - start proxies browser in headless mode (specifically). Default is normal mode

> python fp.py -pb -pu "https://your_website.com/" -ts 240 -mb 5 -bm headless


## Example Command (proxy grab)

The following command will perform these actions:

 - grab HTTP proxies

 - Do not check for dead proxies: optimal, faster

 - Save only 50 proxies to file (limit)

 - Save into custom filename (default name = proxies.txt)

> python fp.py -t http -l 50 --filename your_filename_without_spaces.txt -nocheck


## Example Command (proxy browser after grab)

The following command will perform these actions:

 - grab HTTP proxies

 - Do not check for dead proxies: optimal, faster

 - Save only 50 proxies to file (limit)

 - start 5 proxied browsers, with your url for 240 seconds

 - start proxies browser in normal mode (specifically). Default is normal mode

> python fp.py -t http -l 50 -nocheck -pb -pu https://www.yoursite.com/ -ts 240 -mb 5 -bm normal


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

## Suggestions / Issues / Requests
Please post an issue here: https://github.com/ProHackTech/FreshProxies/issues with appropriate label (optional). You can post feature requests, bugs, performance issues, feedbacks, ask help, your improvements, documentation help or improvements etc.
