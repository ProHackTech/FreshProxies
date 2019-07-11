<h1 align="center">
	<br>
	<img src="https://raw.githubusercontent.com/ProHackTech/FreshProxies/master/git_assets/logo.png" alt="FreshProxy Logo">
	<br>
	FreshProxy
</h1>

Python script to grab HTTP, HTTPS, SOCKS4 and SOCKS5 proxies fast.

## Instructions

You need the following python packages installed:

- argparse

- selenium

You will need Firefox installed on the system

### How To

#### Video Demonstration

<h3 align="center">
	<a href="https://www.youtube.com/watch?v=PlC5wXNXg1A" target="_blank">
		<img src="http://img.youtube.com/vi/PlC5wXNXg1A/0.jpg" alt="FreshProxy Demo" width="480" height="360" border="10" />
	</a>
</h3>

#### HTTP Proxy

> python fp.py --type http

#### HTTPS Proxy

> python fp.py -t https

#### SOCKS4 Proxy

> python fp.py -t socks4

#### SOCKS5 Proxy

> python fp.py -t socks5

#### ALL Proxies

**NOTE**: This option gives error with http proxy grabbing, but all others are grabbed. Run this and then grab http proxy using "--type http" manually.

> python fp.py -t all

## Planned features

[-] Allow users to enter the number of proxies to download

[-] Add support for other proxy websites