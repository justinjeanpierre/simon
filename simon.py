#!/usr/bin/python

import os
from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
Bootstrap(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='xBeXxg9lyElUgwZT6AZ0A',
    consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@app.route('/')
def index():
    tweets = None
    if g.user is not None:
        resp = twitter.request('statuses/home_timeline.json')
        if resp.status == 200:
            tweets = resp.data
        else:
            flash('Unable to load tweets from Twitter.')
    return render_template('index.html', tweets=tweets)

@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('index'))

# jobs routes
@app.route('/jobs', methods=['GET'])
def get_jobs():
#	get a list of all jobs
#	(...to which this authenticated user has access)
    return 'this is a response to a GET request', 200
    
@app.route('/jobs', methods=['POST'])
def post_job():
#	create a job
    return 'this is a response to a POST request', 200
    
@app.route('/jobs', methods=['PUT'])
def put_job():
#	update some job's status
    return 'this is a response to a PUT request', 200
    
@app.route('/jobs', methods=['PUT'])
def delete_job():
#	delete a job
    return 'this is a response to a DELETE request', 200
    
# results routes
@app.route('/results', methods=['GET'])
def get_results():
#	get a list of all results
#	(...to which this authenticated user has access)
    return 'this is a response to a GET request to /results', 200

# stats routes
@app.route('/stats', methods=['GET'])
def get_stats():
#	get the dashboard?
    return 'this is a response to a GET request to /stats', 200

# show the documentation
@app.route('/docs', methods=['GET'])
def show_docs():
    return 'unimplemented', 501

	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)