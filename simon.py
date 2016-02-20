#!/usr/bin/python

import os
from flask import Flask, request, redirect, url_for, send_from_directory
app = Flask(__name__, static_folder='')

"""
@api {get} /user/:id
"""
@app.route("/")
def hello():
	return "Hello World!"

@app.route('/docs')
def show_docs():
	return app.send_static_file('static/index.html')

@app.route('/api_data.js')
def send_api_data():
	print 'static/api_data.js?' + request.query_string
	return app.send_static_file('static/api_data.js')

@app.route('/api_project.js')
def send_api_project():
	print 'static/api_project.js?' + request.query_string
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
