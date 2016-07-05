from flask import render_template, redirect, url_for
from app import app
from .forms import VideoURLForm
from .twitchChatParser import parseTwitchChat, getVideoIdFromURL


@app.route('/', methods=['GET', 'POST'])
def index():
	form = VideoURLForm()
	if form.validate_on_submit():
		return redirect(url_for('vod', videoId=getVideoIdFromURL(form.videoURL.data)))

	return render_template('index.html', 
							title='Home',
							form=form)

@app.route('/v/<videoId>', methods=['GET', 'POST'])
def vod(videoId):
	form = VideoURLForm()
	plotScript, plotDiv = parseTwitchChat(videoId)
	vods = [
		{
			'videoId' : 'v'+videoId,
			'plotScript' : plotScript,
			'plotDiv' : plotDiv
		}
	]
	return render_template('vod.html', 
							title='test',
							form=form,
							vods=vods)
