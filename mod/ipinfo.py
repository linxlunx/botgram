#!/usr/bin/env python

import urllib2
import json

def ipinfo(data):
	'''
	Get ip address info from http://ipinfo.io
	format message:
	/whois <ip address>
	e.g: /whois 8.8.8.8
	'''
	ip_addr = data['text'].split()[1]

	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'curl')]
	get_info = opener.open('http://ipinfo.io/{0}'.format(ip_addr)).read()

	parsed = json.loads(get_info)
	send_text = 'ip: {0} | org: {1} | country: {2}'.format(ip_addr, parsed['org'], parsed['country'])

	return send_text