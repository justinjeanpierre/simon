#!/usr/bin/python

import os
from flask import Flask, request, url_for

app = Flask(__name__, static_folder='')

@app.route("/")
def hello():
	return "Hello World!"

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

# the following routes 
# handle serving apiDoc's
# static files.
@app.route('/docs')
def show_docs():
	return app.send_static_file('static/index.html')

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

@app.route('/main.js')
def send_main_js():
	return app.send_static_file('static/main.js')
	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
