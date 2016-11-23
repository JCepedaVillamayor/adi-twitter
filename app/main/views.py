from flask import Flask, request, redirect, url_for, g, session, flash, render_template, jsonify
from flask_oauthlib.client import OAuth
import json
from . import main, twitter
from .forms import TweetForm, RetweetForm, DeleteForm, FollowForm

TIMELINE_URL = "https://api.twitter.com/1.1/statuses/home_timeline.json"
DELETE_URL = 'https://api.twitter.com/1.1/statuses/destroy/{}.json'
RETWEET_URL = 'https://api.twitter.com/1.1/statuses/retweet/{}.json'
FOLLOW_URL = 'https://api.twitter.com/1.1/friendships/create.json'
TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

@twitter.tokengetter
def get_twitter_token(token=None):
    ''' Obtain token for the current session'''
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@main.before_request
def before_request():
    ''' clean last session to include the new one '''
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']

@main.route('/')
def index():
    ''' main page '''
    tweets = None
    forms = {}
    forms['tweet'] = TweetForm()
    forms['retweet'] = RetweetForm()
    forms['delete'] = DeleteForm()
    forms['follow'] = FollowForm()
    if g.user is not None:
        req = twitter.get(TIMELINE_URL, data={"count":"20"})
        tweets = parse_tweets(req.data) if req.status == 200 else None
    return render_template('index.html', forms=forms, tweets=tweets)

def parse_tweets(data):
    tweets = []
    for raw in data:
        tw = {'text': raw['text'],
              'id': raw['id_str'],
              'name': raw['user']['name'],
              'name_id': raw['user']['id_str'],
              'user_name': raw['user']['screen_name']}
        tweets.append(tw)
    return tweets

@main.route('/login')
def login():
    ''' Get auth token (request) '''
    callback_url=url_for('.oauthorized', next=request.args.get('next'))
    flash('logueado correctamente')
    return twitter.authorize(callback=callback_url
                             or request.referrer or None)

@main.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('.index'))

# Callback
@main.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('.index'))

@main.route('/op1', methods=['POST'])
def deleteTweet():
    form = DeleteForm()
    if g.user is None:
        return redirect(url_for('.login'))
    if form.validate_on_submit():
        tweet_id = form.tweet_id.data
        session = g.user
        req = twitter.post(DELETE_URL.format(tweet_id))
        if req.status == 200:
            flash('Tweet removed successfully')
        else:
            flash('Sorry, the tweet couldn\'t be removed')
    return redirect(url_for('.index'))

@main.route('/op2', methods=['POST'])
def retweet():
    form = RetweetForm()
    if g.user is None:
        return redirect(url_for('.login'))
    if form.validate_on_submit():
        tweet_id = form.tweet_id.data
        session = g.user
        req = twitter.post(RETWEET_URL.format(tweet_id))
        if req.status == 200:
            flash('Tweet retweeted successfully')
        else:
            flash('Sorry, the tweet couldn\'t be retweeted')
    return redirect(url_for('.index'))

@main.route('/op3', methods=['POST'])
def follow():
    form = FollowForm()
    if g.user is None:
        return redirect(url_for('.login'))
    if form.validate_on_submit():
        print form.username.data
        print form.user_id.data
        data = generate_follow_json(form)
        req = twitter.post(FOLLOW_URL, data=data)
        print req.status
        if req.status == 200:
            flash('User Followed successfully')
        else:
            flash('Sorry, the user couldn\'t be followed')
    else:
        flash('Invalid form')
    return redirect(url_for('.index'))

def generate_follow_json(form):
    data = {'follow': True}
    if form.username.data != '':
        if form.user_id.data != '':
            data['user_id'] = form.user_id.data
    if form.user_id.data != '':
        if form.username.data != '':
            data['screen_name'] = form.username.data
    return data

@main.route('/op4', methods=['POST'])
def tweet():
    form = TweetForm()
    if g.user is None:
        return redirect(url_for('.login'))
    if form.validate_on_submit():
        tuit = form.tweet_text.data
        session = g.user
        req = twitter.post(TWEET_URL, data={'status': tuit})
        if req.status == 200:
            flash('Tweet updated successfully')
        else:
            flash('Sorry, the tweet couldn\'t be updated')
    else:
        flash("Sorry, you have exceeded the maximum amount of tweets")
    return redirect(url_for('.index'))
