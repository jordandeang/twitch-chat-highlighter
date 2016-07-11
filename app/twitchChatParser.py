#!venv/bin/python
# -*- coding: utf-8 -*-
import requests, sys, datetime, json, string
from bokeh.layouts import column
from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models import HoverTool, TapTool, CrosshairTool, PanTool, WheelZoomTool, NumeralTickFormatter, CustomJS, Circle
import numpy as numpy
from numpy import ones, convolve
from bokeh.embed import components

# Parses the given URL to retrieve the video ID
def getVideoIdFromURL(videoURL):

	# Video id input parsed from videoURL
	return videoURL[string.index(videoURL, '/v/'):][3:]

def movingaverage(interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')

# Retrieves the chat from the given VOD and returns an a tuple script, div that create the bokeh plot
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
	for timestamp in xrange(start,stop, 30):

		# Request messages from Twitch
		response = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(timestamp) + '&video_id=v' + videoId).json()
		data = response['data']

		bucketOne = 0 
		bucketTwo = 0
		bucketThree = 0
		# Add to list
		for message in data:
			if message['attributes']['timestamp'] < (timestamp*1000) + 10000:
				bucketOne += 1
			elif message['attributes']['timestamp'] >= (timestamp*1000) + 10000 and message['attributes']['timestamp'] < (timestamp*1000) + 20000:
				bucketTwo += 1
			else:
				bucketThree += 1
				
		concentrationByTime.append(
			(timestamp - start, bucketOne)
		)
		concentrationByTime.append(
			(timestamp - start + 10, bucketTwo)
		)
		concentrationByTime.append(
			(timestamp - start + 20, bucketThree)
		)

		# Write out current progress to stdout
		sys.stdout.write("\r%d%%" % ( (float(timestamp - start) / float(stop- start)) * 100))
		sys.stdout.flush() 

	# VOD Times
	x = [a[0] for a in concentrationByTime]

	# # of Twitch Chat messages
	rawY = [a[1] for a in concentrationByTime]
	newY = movingaverage(rawY, 3)

	# # Requests VOD title
	videoTitle = requests.get('https://api.twitch.tv/kraken/videos/v' + videoId).json()['title']

	# Bokeh stuff
	patchX = list(x)
	patchX.insert(0, x[0])
	patchX.append(x[len(x)-1])
	patchY = list(newY)
	patchY.insert(0, 0)
	patchY.append(0)
	timeF = [str(datetime.timedelta(seconds=i)) for i in x]
	source = ColumnDataSource(data=dict(x=x, y=newY, timeF=timeF, rawY=rawY))

	tapCallback = CustomJS(args=dict(source=source), code="""
				var seekTime = source.get('data')['x'][cb_obj.get('selected')['1d'].indices];
				if (seekTime > 0){
					player.seek(seekTime-5);
				}else{
					player.seek(0);
				}
				""")

	if (x[len(x)-1] < 1800):
		p = figure(width=1024, height=280, title=videoTitle,tools="reset")
	else:
		p = figure(width=1024, height=280, x_range=(0, 1800), title=videoTitle,tools="reset")

	p.xaxis[0].axis_label = 'VOD Time'
	p.xaxis[0].formatter = NumeralTickFormatter(format='00:00:00')
	p.yaxis[0].axis_label = 'Number of Twitch Chat Messages'
	p.patch(x=patchX, y=patchY, color="#B3DE69",line_color="#009900", line_width=1.2)
	p.diamond('x','y', size=12, color="#0000b2", source=source, alpha=0.1, hover_alpha=1.0)
	invisible_circle = Circle(x='x', y='y', fill_color='gray', fill_alpha=0, line_color=None, size=6)
	cr = p.add_glyph(source, invisible_circle)


	p.add_tools(HoverTool(tooltips=[('Timestamp', '@timeF'),('Avg # of Messages', '@y')],  renderers=[cr], mode='vline'))
	p.add_tools(TapTool(callback=tapCallback))
	p.add_tools(CrosshairTool(dimensions=['height']))
	p.add_tools(PanTool(dimensions=['width']))
	p.add_tools(WheelZoomTool(dimensions=['width']))
	return components(p)