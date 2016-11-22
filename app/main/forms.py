from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, \
    ValidationError

class TweetForm(FlaskForm):
    tweet_text = StringField('Tweet', validators=[DataRequired()])
    submit = SubmitField('Submit')
