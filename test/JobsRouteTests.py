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
		self.test_job.owner = 'test_JOBS_ROUTE_TESTS_owner'
		self.test_job.status = 'test_JOBS_ROUTE_TESTS_status'

		# create some test data
		self.jobs.insert_one({'identifier':str(1001), 'owner':'test_JOBS_ROUTE_TESTS_owner', 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1002), 'owner':str(115122217971165854689), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1003), 'owner':str(115122217971165854689), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1004), 'owner':str(115122217971165854689), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1005), 'owner':str(2593451828), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1006), 'owner':str(2593451828), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1007), 'owner':str(2593451828), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		self.jobs.insert_one({'identifier':str(1008), 'owner':str(2593451828), 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
			
	def tearDown(self):
		# remove test data from test db
		self.jobs.delete_many({'owner':'test_JOBS_ROUTE_TESTS_owner'})
		self.jobs.delete_many({'owner':str(115122217971165854689)})
		self.jobs.delete_many({'owner':str(2593451828)})
	
	def test_get_job(self):
		response = self.app.get('/jobs/1001')
		
		assert response.status == '401 UNAUTHORIZED'

	def test_get_jobs(self):
		response = self.app.get('/jobs')
		
		assert response.status == '401 UNAUTHORIZED'


class JobsRouteTestCasePOST(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()
		
	def tearDown(self):
		pass
		
	def test_post_job_no_data(self):
		response = self.app.post('/jobs')
		
		assert response.status == '401 UNAUTHORIZED'

	def test_post_job_with_params(self):
		d = dict(maximum_frequency=1000)
		response = self.app.post('/jobs', data=d)
		
		assert response.status == '401 UNAUTHORIZED'


if __name__ == '__main__':
	unittest.main()
