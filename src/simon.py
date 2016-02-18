#!/usr/bin/python

import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

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

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
