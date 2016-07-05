from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class VideoURLForm(Form):
	videoURL = StringField('videoURL', validators=[DataRequired()])