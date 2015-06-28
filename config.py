#!/usr/bin/env python

# Setting token and register module
# Please include the module information

from mod.ipinfo import ipinfo

config = {
	'token' : 'Use your own telegram bot token',
	'module' : {
		'/whois' : (ipinfo, 'Getting ip address information', 'e.g: /whois 8.8.8.8'),
	}
}
