#!/usr/bin/python

import Job
import Result
import Config
from Config import DevelopmentConfig, TestingConfig

import os, json, ast
import jsonpickle
from flask import Flask, jsonify
from flask import g, session, request, url_for, flash
from flask import redirect, render_template

# OAuth
from flask_oauthlib.client import OAuth, OAuthException

# persistence
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

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
# app.config.from_object(Config.DevelopmentConfig)
app.config.from_object(Config.TestingConfig)

# db startup and variables
client = MongoClient(TestingConfig.MONGO_URI)
db = client[TestingConfig.MONGO_DBNAME]
jobs = db.jobs
results = db.results


# persistence
# mongo = PyMongo(app)
@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']['user_id']
    elif 'google_token' in session:
        g.user = json.loads(getattr(google.get('userinfo'), 'raw_data'))['id']
    elif 'facebook_token' in session:
        g.user = json.loads(getattr(facebook.get('/me'), 'raw_data'))['id']

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
        g.user = resp['user_id']
        
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
    g.user = json.loads(getattr(me, 'raw_data'))['id']
    
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

    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    g.user = json.loads(getattr(me, 'raw_data'))['id']

    return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

""" 
--------------------------------------------
Form functions
--------------------------------------------
"""

# jobs routes
@app.route('/jobs', methods=['GET'])
def get_jobs():
#   get the authenticated user's jobs

    if g.user is not None:
        user_jobs = Job.Job.find_by_user_id(g.user, jobs)
        
        if user_jobs is not None:
            return jsonpickle.encode(user_jobs), 200
        else:
            return '', 501
    else:
        return '', 401

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
#   get a specific job

    job = Job.Job.find_by_id(str(job_id), g.user, jobs)
    
    if g.user is None:
        return '', 401

    if job is not None:
        return jsonpickle.encode(job), 200
    else:
        return 'Invalid or unauthorized id: ' + str(job_id), 404
    
@app.route('/jobs', methods=['POST'])
def post_job():
    
    # make sure user is authenticated
    if g.user is None:
        return '', 401
    
    if len(request.form.keys()) == 0:
        # request must have simulator parameters.
        return '', 400
    else:
        # create a Job object
        job = Job.Job()
        # set the owner to the current user
        job.owner = g.user
        # populate with supplied parameters
        job.update(request.form)
        # save to db
        new_job_id = job.save(jobs)
        # send to simulator
        job.submit() # callback?
        
        return jsonpickle.encode({'identifier':new_job_id}), 200
    
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
#   get a list of all results to which this authenticated user has access

    if g.user is not None:
        user_results = Result.Result.find_by_user_id(g.user, results)
        
        if user_results is not None:
            return jsonpickle.encode(user_results), 200
        else:
            return '', 501
    else:
        return '', 401

    return render_template('results.html')

@app.route('/results/<result_id>', methods=['GET'])
def get_result(result_id):
#   get one of the user's results

    result =  Result.Result.find_by_id(str(result_id), g.user, results)

    if g.user is None:
        return '', 401

    if result is not None:
        return jsonpickle.encode(result), 200
    else:
        return 'Invalid or unauthorized id: ' + str(result_id), 404
    
@app.route('/results', methods=['POST'])
def post_result():
    
    if len(request.form.keys()) == 0:
        return '', 400
    else:
        # create a Result object
        result = Result.Result()
        
        # populate it
        result.update(request.form)
        # save it
        new_result_id = result.save(results)        

        return jsonpickle.encode({'identifier':new_result_id}), 200 # should return new Result's id

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
    session.pop('facebook_token', None)
    return redirect(url_for('index'))

# show the documentation
@app.route('/docs', methods=['GET'])
def show_docs():
    return render_template('docs.html')

@app.route('/developers', methods=['GET'])
def show_dev():
    return render_template('dev.html')

@app.route('/faq', methods=['GET'])
def show_faq():
    return render_template('faq.html')

@app.route('/run', methods=['GET'])
def run_simulation():
    return render_template('simulation.html')

"""
--------------------------------------------
app startup
--------------------------------------------
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
