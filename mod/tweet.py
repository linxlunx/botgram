#!/usr/bin/env python

import oauth2 as oauth
import urllib

def tweet(data):
	'''
		Receive message and then tweet!
		Do not forget to fill the access key!
		e.g: /tweet hi, my name is sherina
	'''

	text = ' '.join(data['text'].split()[1:])

	####### FILL THESE VARIABLES WITH YOURS #########
	consumer_key = ''
	consumer_secret = ''
	access_key = ''
	access_secret = ''
	#################################################

	consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
	token = oauth.Token(key=access_key, secret=access_secret)
	client = oauth.Client(consumer, token)

	data = urllib.urlencode({'status': text})
	header, response = client.request("https://api.twitter.com/1.1/statuses/update.json", body=data,method="POST")
	send_text = 'Tweeted!'
	return send_text