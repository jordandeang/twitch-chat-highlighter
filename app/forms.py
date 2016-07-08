from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, URL, ValidationError
from app.twitchChatParser import getVideoIdFromURL

def isTwitchVOD(form, field):
	if 'twitch.tv/' in field.data and '/v/' in field.data:
		try:
			getVideoIdFromURL(field.data)
		except:
			raise ValidationError("Not a valid Twitch VOD URL")
	else:
		raise ValidationError("Not a valid Twitch VOD URL")

class VideoURLForm(Form):
	videoURL = StringField('videoURL', validators=[InputRequired(), URL(), isTwitchVOD])