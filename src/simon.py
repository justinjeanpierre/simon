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

# here is some sample API documentation:
"""
@apiVersion 0.0.1
"""

"""
@api {get} /user/:id Request User information
@apiName GetUser
@apiGroup User

@apiParam {Number} id Users unique ID.

@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.
"""

# jobs routes
@app.route('/jobs', methods=['GET'])
def get_jobs():
#	get a list of all jobs
#	(...to which this authenticated user has access)
    return 'this is a response to a GET request'
    
@app.route('/jobs', methods=['POST'])
def post_job():
#	create a job
    return 'this is a response to a POST request'
    
@app.route('/jobs', methods=['PUT'])
def put_job():
#	update some job status
    return 'this is a response to a PUT request'	

# users routes
@app.route('/users', methods=['GET'])
def get_users():
#	get a user's details?
    return 'this is a response to a GET request to /users'
    
@app.route('/users', methods=['POST'])
def post_user():
#	create a user
    return 'this is a response to a POST request to /users'
    
@app.route('/users', methods=['PUT'])
def put_user():
#	update some user status
    return 'this is a response to a PUT request to /users'	

# The following routes handle serving apiDoc's static files.
# This is brittle and we should find a better way to serve
# templates and static files.
@app.route('/docs')
def show_docs():
	return render_template('bootdoc.html')

@app.route('/api_data.js') # what about the request string?
def send_api_data():
	return app.send_static_file('static/api_data.js')

@app.route('/api_project.js') # what about the request string?
def send_api_project():
	return app.send_static_file('static/api_project.js')

@app.route('/css/<filename>')
def send_css(filename):
	return app.send_static_file('static/' + url_for('static', filename='css/' + filename))

@app.route('/locales/<path:filename>')
def send_locales(filename):
	return app.send_static_file('static/' + url_for('static', filename='locales/' + filename))

@app.route('/utils/<path:filename>')
def send_utils(filename):
	return app.send_static_file('static/' + url_for('static', filename='utils/' + filename))

@app.route('/vendor/<path:filename>')
def send_vendor(filename):
	return app.send_static_file('static/' + url_for('static', filename='vendor/' + filename))

@app.route('/img/<path:filename>')
def send_image(filename):
    return app.send_static_file('static/' + url_for('static', filename='img/' + filename))

@app.route('/main.js')
def send_main_js():
	return app.send_static_file('static/main.js')
	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)