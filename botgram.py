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
		self.database = 'telegram_research'
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
					if 'text' in temp['message']:
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
		# Send message function, receive any output from command
		uri = '/sendMessage'
		post_data = urllib.urlencode({
				'chat_id' : chat_id,
				'text' : text,
			})
		send_message_url = '{0}{1}'.format(self.full_url, uri)
		urllib2.urlopen(send_message_url, post_data)
		return True

	def get_help(self):
		# Special command for command list, exclude from module
		help_text = '{0}    {1}\n'.format('/help', 'Help and command list')
		for i in self.module:
			help_text += '{0}    {1}\n'.format(i, self.module[i][1])
		return help_text

	def execute(self, list_update):
		# Execute command when receive message
		for i in list_update:
			parse_text = i['text'].split()
			try:
				command = parse_text[0]
				# Special help command for list command and it's description
				if command == '/help':
					# if command length more than one, than show example
					if len(parse_text) > 1:
						if '/{0}'.format(parse_text[1]) not in self.module:
							print 'command not registered'
						help_list = self.module['/{0}'.format(parse_text[1])][2]
					else:
						help_list = self.get_help()
					self.send_message(i['chat_id'], help_list)
				# if not help, check the module, if exists, execute module
				else:
					if command not in self.module:
						print 'command not registered'
					text_message = self.module[command][0](i)
					self.send_message(i['chat_id'], text_message)
			except Exception, e:
				print e
				print 'command not registered'

if __name__ == '__main__':
	tele = Tele()
	data = tele.checkId()
	if data:
		tele.execute(data)
