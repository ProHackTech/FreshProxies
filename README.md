# FastProxy

Python script to grab HTTP, HTTPS, SOCKS4 and SOCKS5 proxies fast.

## Instructions

You need the following python packages installed:

- argparse

- selenium

You will need Firefox installed on the system

### How To

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

[] Allow users to enter the number of proxies to download

[] Add support for other proxy websites