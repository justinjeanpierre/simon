#!/usr/bin/python

import Job
import Config
import os, json
from flask import Flask, jsonify
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from Config import DevelopmentConfig
from flask_oauthlib.client import OAuth, OAuthException

""" 
--------------------------------------------
App Initialization
--------------------------------------------
"""

# Current project folder
current_dir = os.getcwd()
# Path to templates folder
template_dir = os.path.join(current_dir, 'templates')
# Path to static folder
static_dir = os.path.join(current_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# change this when pushing to production
# app.config.from_object(Config.ProductionConfig)
app.config.from_object(Config.DevelopmentConfig)

@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']
    elif 'google_token' in session:
        g.user = session['google_token']
    elif 'oauth_token' in session:
        g.user = session['oauth_token']

""" 
--------------------------------------------
Twitter Login 
--------------------------------------------
"""

twitter = oauth.remote_app(
    'twitter',
    consumer_key=DevelopmentConfig.TWITTER_KEY,
    consumer_secret=DevelopmentConfig.TWITTER_SECRET,
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

@app.route('/twitter/')
def twitter_login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('index'))

""" 
--------------------------------------------
Google Login
--------------------------------------------
"""

app.config['GOOGLE_ID'] = DevelopmentConfig.GOOGLE_KEY
app.config['GOOGLE_SECRET'] = DevelopmentConfig.GOOGLE_SECRET

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/google')
def google_login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/google/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return redirect(url_for('index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

""" 
--------------------------------------------
Facebook Login
--------------------------------------------
"""

FACEBOOK_APP_ID = DevelopmentConfig.FACEBOOK_KEY
FACEBOOK_APP_SECRET = DevelopmentConfig.FACEBOOK_SECRET

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

@app.route('/facebook')
def facebook_login():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/facebook/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

""" 
--------------------------------------------
Form functions
--------------------------------------------
"""

# jobs routes
@app.route('/jobs', methods=['GET'])
def get_jobs():
#   get a list of all jobs
#   (...to which this authenticated user has access)
    return '', 501
   
@app.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
#   get a specific job
    return job_id, 501
    
@app.route('/jobs', methods=['POST'])
def post_job():
	# create a job
    # to submit a job:
    # get request parameters (form data?)
    # create object, populate with request data
    # save in db
    # serialize and send to simulator
    job = Job.Job()
    user_input = request.form
    job.update(user_input)
    
    if len(user_input.keys()) == 0:
        # this is a request sent without
        # simulator parameters.
        # it should be rejected.
        return '', 400
    else:
        return json.dumps(user_input), 200
    
@app.route('/jobs/<job_id>', methods=['PUT'])
def put_job(job_id):
#   update some job's status
    return job_id, 501
    
@app.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
#   delete a job
    return job_id, 501
    
# results routes
@app.route('/results', methods=['GET'])
def get_results():
#   get a list of all results
#   (...to which this authenticated user has access)

    return render_template('results.html')

@app.route('/results/<result_id>', methods=['GET'])
def get_result(result_id):
#   get one of the user's results
    return result_id, 501

# stats routes
@app.route('/stats', methods=['GET'])
def get_stats():
#   get the dashboard?
    return '', 501

""" 
--------------------------------------------
Main website routes
--------------------------------------------
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('twitter_oauth', None)
    session.pop('oauth_token', None)
    return redirect(url_for('index'))

# show the documentation
@app.route('/docs', methods=['GET'])
def show_docs():
    return '', 501

@app.route('/run', methods=['GET'])
def run_simulation():
    return render_template('simulation.html')

	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
