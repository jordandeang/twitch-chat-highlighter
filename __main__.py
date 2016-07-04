#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, time, json

# Video id input (prefixed 'v' is optional)
videoId = 'v' + sys.argv[1].replace('v', '')

# Get start and stop time by looking at the 'detail' message from Twitch
response = requests.get('https://rechat.twitch.tv/rechat-messages?start=0&video_id=' + videoId).json()

# Get 'detail' message and split it
detail = response['errors'][0]['detail'].split(' ')

# Start and stop timestamps
start = int(detail[4])
stop = int(detail[6])

# Used message ids
#messageIds = []

# For every 30 seconds, start to stop; request chat messages
for timestamp in xrange(start, stop, 30):

	# Request messages from Twitch
	response = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(timestamp) + '&video_id=' + videoId).json()
	data = response['data']

	print len(data)
	print time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(timestamp))