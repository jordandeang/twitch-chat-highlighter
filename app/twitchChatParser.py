#!venv/bin/python
# -*- coding: utf-8 -*-
import requests, sys, datetime, json, string
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, NumeralTickFormatter
from bokeh.resources import CDN
from bokeh.embed import components

# Parses the given URL to retrieve the video ID
def getVideoIdFromURL(videoURL):
	# Video id input parsed from videoURL
	return videoURL[string.index(videoURL, '/v/'):][3:]

# Retrieves the chat from the given VOD and returns an HTML plot of the data
def parseTwitchChat(videoId):

	# Get start and stop time by looking at the 'detail' message from Twitch
	response = requests.get('https://rechat.twitch.tv/rechat-messages?start=0&video_id=v' + videoId).json()

	# Get 'detail' message and split it
	detail = response['errors'][0]['detail'].split(' ')

	# Start and stop timestamps
	start = int(detail[4])
	stop = int(detail[6])

	# List of tuples of format (VOD Time, number of twitch chat messages)
	concentrationByTime = []

	# For every 30 seconds, start to stop; request chat messages
	for timestamp in xrange(start, start+1000, 30):

		# Request messages from Twitch
		response = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(timestamp) + '&video_id=v' + videoId).json()
		data = response['data']


		concentrationByTime.append(
			(timestamp - start, len(data))
		)

		sys.stdout.write("\r%d%%" % ( (float(timestamp - start) / float(stop- start)) * 100))
		sys.stdout.flush() 


	x = [a[0] for a in concentrationByTime]
	y = [a[1] for a in concentrationByTime]

	# # Requests VOD title
	videoTitle = requests.get('https://api.twitch.tv/kraken/videos/v' + videoId).json()['title']

	# Bokeh stuff
	right = list(x)
	right.pop(0)
	right.append(1000)
	timeX = [str(datetime.timedelta(seconds=i)) for i in x]

	source = ColumnDataSource(data=dict(time=timeX))

	p = figure(width=800, height=250, title = videoTitle, x_axis_type='datetime')
	p.xaxis[0].axis_label = 'VOD Time'
	p.xaxis[0].formatter = NumeralTickFormatter(format='00:00:00')
	p.yaxis[0].axis_label = 'Number of Twitch Chat Messages'
	qr = p.quad(top=y, bottom=0, left=x, right=right, color="#B3DE69", hover_fill_color="firebrick", source=source)
	p.add_tools(HoverTool(tooltips=[('Timestamp', '@time'),('# of New Messages', '@top')], renderers=[qr], mode='mouse'))
	return components(p)