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

class PersistenceTestCase(unittest.TestCase):
		
	def setUp(self):
		# initialization stuff
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.jobs = self.db.jobs
		
		self.test_job = Job.Job()
		test_job = {'identifier':'test_job_identifier'}
		test_job = {'identifier':987654321}
		self.jobs.insert_one(test_job)

	def tearDown(self):
		# remove test data from test db
		self.jobs.delete_many({'identifier':'test_job_identifier'})
		self.jobs.delete_many({'identifier':987654321})
		
	def test_retrieve_job(self):
		# get a job back from the test db
		_job = Job.Job.find_job(987654321, self.jobs)
		
		assert _job is not None
		assert _job.id == 987654321

if __name__ == '__main__':
	unittest.main()
