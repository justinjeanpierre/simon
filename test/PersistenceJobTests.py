#!/usr/bin/python

import os	
import unittest
from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig
import json

import simon
import Job

class JobPersistenceTestCase(unittest.TestCase):
		
	def setUp(self):
		# initialization stuff
		# make sure mongod is running first!!!
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.jobs = self.db.jobs
		
		self.test_job = Job.Job()
		test_job = {'identifier':'test_job_identifier'}
		test_job = {'identifier':987654321}
		self.jobs.insert_one(test_job)

		# some available stuff
		self.test_store_job_identifier = 8765
		
	def tearDown(self):
		# remove test data from test db
		self.jobs.delete_many({'identifier':'test_job_identifier'})
		self.jobs.delete_many({'identifier':987654321})
		self.jobs.delete_many({'identifier':self.test_store_job_identifier})
		
	def test_retrieve_job(self):
		# get a job back from the test db
		_job = Job.Job.find_by_id(987654321, self.jobs)
		
		assert _job is not None
		assert _job.id == 987654321
		
	def test_store_job(self):
		_job = Job.Job()
		
		# reassurance
		assert _job is not None
		assert _job.id == ''
		assert _job.owner == ''
		assert _job.status == ''
		
		# save the job
		_job.id = self.test_store_job_identifier
		_job.save(self.jobs)
		
		# create an "empty" job
		saved_job = Job.Job()
		
		# populate the empty job with db data
		res = self.jobs.find_one({'identifier':_job.id}) 
		if res is not None:
			saved_job.id = res['identifier']
			saved_job.simulator_parameters = res['simulator_parameters']
		
		# compare db data with test job
		assert saved_job is not None
		assert saved_job.id == self.test_store_job_identifier
		assert saved_job.simulator_parameters == _job.simulator_parameters


if __name__ == '__main__':
	unittest.main()
