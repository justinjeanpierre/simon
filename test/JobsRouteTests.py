#!/usr/bin/python

import os	
import unittest

from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig

import simon
import Job

class JobsRouteTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()

	def test_put_job(self):
		response = self.app.put('/jobs/345')
		
		assert response.status == '501 NOT IMPLEMENTED'

	def test_delete_job(self):
		response = self.app.delete('/jobs/567')
		
		assert response.status == '501 NOT IMPLEMENTED'


class JobsRouteTestCaseGET(unittest.TestCase):

	def setUp(self):
		self.app = simon.app.test_client()

		# initialization stuff
		# make sure mongod is running first!!!
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.jobs = self.db.jobs
		
		self.test_job = Job.Job()
		self.test_job.id = str(24680)
		self.test_job.owner = 'test_JOBS_ROUTE_TESTS_owner'
		self.test_job.status = 'test_JOBS_ROUTE_TESTS_status'
		
		self.jobs.insert_one({'identifier':self.test_job.id, 'owner':self.test_job.owner, 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
			
	def tearDown(self):
		# remove test data from test db
		self.jobs.delete_many({'identifier':self.test_job.id})
		pass
	
	def test_get_job(self):
		response = self.app.get('/jobs/24680')
		
		assert '24680' in response.data
		assert response.status == '200 OK'

	def test_get_jobs(self):
		response = self.app.get('/jobs')
		
		assert response.status == '501 NOT IMPLEMENTED'


class JobsRouteTestCasePOST(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()
		
	def tearDown(self):
		pass
		
	def test_post_job_no_data(self):
		response = self.app.post('/jobs')
		
		assert response.status == '400 BAD REQUEST'

	def test_post_job_with_params(self):
		d = dict(maximum_frequency=1000)
		response = self.app.post('/jobs', data=d)
		
		assert '\"maximum_frequency\": \"1000\"' in response.data
		assert response.status == '200 OK'


if __name__ == '__main__':
	unittest.main()
