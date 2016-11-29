from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class TweetForm(FlaskForm):
    tweet_text = StringField('Tweet Form', validators=[DataRequired(), Length(1,140)])

class RetweetForm(FlaskForm):
    tweet_id = IntegerField('Retweet Form', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    tweet_id = IntegerField('Delete Form', validators=[DataRequired()])

class FollowForm(FlaskForm):
    username = StringField('Follow Form', validators=[DataRequired()], description='username' )
    user_id = StringField('', validators=[DataRequired()], description='user id')
