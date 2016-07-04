#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, datetime, time, json
import plotly as py
import plotly.graph_objs as go

# Video id input (prefixed 'v' is optional)
videoId = 'v' + sys.argv[1].replace('v', '')

# Get start and stop time by looking at the 'detail' message from Twitch
response = requests.get('https://rechat.twitch.tv/rechat-messages?start=0&video_id=' + videoId).json()

# Get 'detail' message and split it
detail = response['errors'][0]['detail'].split(' ')

# Start and stop timestamps
start = int(detail[4])
stop = int(detail[6])

# List of tuples of format (VOD Time, number of twitch chat messages)
concentrationByTime = []

# For every 30 seconds, start to stop; request chat messages
for timestamp in xrange(start, start+2000, 30):

	# Request messages from Twitch
	response = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(timestamp) + '&video_id=' + videoId).json()
	data = response['data']


	concentrationByTime.append(
		(str(datetime.timedelta(seconds = (timestamp - start))), len(data))
	)

	sys.stdout.write("\r%d%%" % ( (float(timestamp - start) / float(stop- start)) * 100))
	sys.stdout.flush() 

# Plotly stuff
x = [a[0] for a in concentrationByTime]
y = [a[1] for a in concentrationByTime]
yText = [str(a) + ' messages' for a in y]

trace1 = go.Bar(
	x = x,
	y = y,
	text =  yText,
	hoverinfo = 'x+text',
	marker=dict(
		color='rgb(158,202,225)',
		line=dict(
			color='rgb(8,48,107)',
			width=1,
		)
	),
	opacity = 0.6
)

# Requests VOD title
videoTitle = requests.get('https://api.twitch.tv/kraken/videos/' + videoId).json()['title']

layout = go.Layout(
	title = videoTitle,
	bargap = 0,
	xaxis = dict(
		title = "VOD Time"
	),
	yaxis = dict(
		title = "Number of Twitch Chat Messages"
	)
)

plotData = [trace1]
fig = go.Figure(data = plotData, layout = layout)
py.offline.plot(fig)