from flask import render_template, redirect, url_for, request, make_response
from app import application
from forms import VideoURLForm
from twitchChatParser import getVideoIdFromURL, parseTwitchChat


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
	form = VideoURLForm()
	if form.validate_on_submit():
		return redirect(url_for('vod', videoId=getVideoIdFromURL(form.videoURL.data)))
	return render_template('index.html', 
							title='Home',
							form=form)

@application.route('/v/<videoId>', methods=['GET', 'POST'])
def vod(videoId):
	form = VideoURLForm()
	if form.validate_on_submit():
		return redirect(url_for('vod', videoId=getVideoIdFromURL(form.videoURL.data)))
	return render_template('vod.html', 
							title='Vod Highlight',
							form=form,
							videoId=videoId)

@application.route('/p', methods=['POST'])
def chatParser():
	if request.method == 'POST':
		videoId = request.form['videoId']
		plotScript, plotDiv = parseTwitchChat(videoId)
		resp = make_response(plotScript+plotDiv)
		resp.headers['Content-Type'] = 'text/html'
		print videoId
		return resp
	else:
		return redirect(url_for('vod', videoId=videoId))