#!/usr/bin/env python

# Setting token and registered module

from mod.ipinfo import ipinfo

config = {
	'token' : 'Use your own telegram bot token',
	'module' : {
		'/whois' : ipinfo,
	}
}
