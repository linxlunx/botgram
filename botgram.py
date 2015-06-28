#!/usr/bin/env python

import pymongo
import urllib2
import urllib
import datetime
import json
from config import config

class Tele:
	def __init__(self):
		# open database connection
		self.database = 'telegram'
		self.client = pymongo.MongoClient()
		self.db = self.client[self.database]

		# set variable
		self.now = datetime.datetime.now().strftime('%Y-%m-%d')
		self.url = 'https://api.telegram.org'
		self.token = config['token']
		self.full_url = '{0}/bot{1}'.format(self.url, self.token)

		# register module
		self.module = config['module']

	def getUpdate(self):
		# Getting Last Update from Telegram
		uri = '/getUpdates'
		get_update_url = '{0}{1}'.format(self.full_url, uri)
		update_data = urllib2.urlopen(get_update_url).read()
		return update_data

	def parseText(self):
		# Convert data to json format
		data_json = self.getUpdate()
		json_data = json.loads(data_json)
		return data_json

	def checkId(self):
		# Check if update_id exist in database
		res = self.parseText()
		results = json.loads(res)
		update_list = []

		if results['result']:
			for temp in results['result']:
				mess_date = datetime.datetime.fromtimestamp(temp['message']['date']).strftime('%Y-%m-%d')
				update_id = temp['update_id']
				chat_id = temp['message']['chat']['id']

				per_id = self.db.chat.find_one({
						'$and' : [
							{'update_id' : update_id},
							{'date' : mess_date},
							{'chat_id' : chat_id},
						]
					})
				if not per_id:
					update_list.append({
							'update_id' : update_id,
							'chat_id' : temp['message']['chat']['id'],
							'text' : temp['message']['text']
						})

					self.db.chat.insert({
							'update_id' : update_id,
							'chat_id' : chat_id,
							'date' : mess_date,
							'text' : temp['message']['text'],
						})

		return update_list


	def send_message(self, chat_id, text):
		uri = '/sendMessage'
		post_data = urllib.urlencode({
				'chat_id' : chat_id,
				'text' : text,
			})
		send_message_url = '{0}{1}'.format(self.full_url, uri)
		urllib2.urlopen(send_message_url, post_data)
		return True

	def execute(self, list_update):
		for i in list_update:
			try:
				command = i['text'].split()[0]
				if command not in self.module:
					print 'command not registered'.format(command)
				text_message = self.module[command](i)
				self.send_message(i['chat_id'], text_message)
			except Exception, e:
				print e
				print 'command not registered'

tele = Tele()
data = tele.checkId()
if data:
	tele.execute(data)
