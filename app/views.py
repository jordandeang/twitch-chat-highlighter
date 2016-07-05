from flask import render_template, redirect
from app import app
from .forms import VideoURLForm
from .twitchChatParser import parseTwitchChat


@app.route('/', methods=['GET', 'POST'])
def index():
	form = VideoURLForm()
	if form.validate_on_submit():
		return redirect('/test')

	vods = [
		{
		'videoId' : 'v75990824',
		'plotScript' : 'nah',
		'plotDiv' : 'plotDiv'
		}
	]
	return render_template('index.html', 
							title='Home',
							form=form,
							vods=vods,)

@app.route('/test', methods=['GET', 'POST'])
def testView():
	form = VideoURLForm()
	plotScript, plotDiv = parseTwitchChat('https://www.twitch.tv/smashstudios/v/75990824')
	vods = [
		{
			'videoId' : 'v75990824',
			'plotScript' : plotScript,
			'plotDiv' : plotDiv
		}
	]
	return render_template('index.html', 
						title='test',
						form=form,
						vods=vods,)
