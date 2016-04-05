#!/usr/bin/python

import os	
import unittest
from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig

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
		self.test_store_job_owner = 'some_user_id'
		self.test_store_job_status = 'SOME_JOB_STATUS'		
		
	def tearDown(self):
		# remove test data from test db
		self.jobs.delete_many({'identifier':'test_job_identifier'})
		self.jobs.delete_many({'identifier':987654321})
		self.jobs.delete_many({'identifier':self.test_store_job_identifier})
		
	def test_store_job(self):
		_job = Job.Job()
		
		# reassurance
		assert _job is not None
		assert _job.id is None
		assert _job.owner is None
		assert _job.status is None
		
		# populate job params
		_job.id = self.test_store_job_identifier
		_job.owner = self.test_store_job_owner
		_job.status = self.test_store_job_status
		
		# save the job
		_job.save(self.jobs)
		
		# create an "empty" job
		# (to compare retrieved data)
		saved_job = Job.Job()
		
		# populate the empty job with db data
		res = self.jobs.find_one({'identifier':_job.id}) 
		if res is not None:
			saved_job.id = res['identifier']
			saved_job.owner = res['owner']
			saved_job.status = res['status']
			saved_job.simulator_parameters = res['simulator_parameters']
		
		# compare db data with test job data
		assert saved_job is not None
		assert saved_job.id == self.test_store_job_identifier
		assert saved_job.owner == self.test_store_job_owner
		assert saved_job.status == self.test_store_job_status
		assert saved_job.simulator_parameters == _job.simulator_parameters
		
	def test_retrieve_job(self): #(not a useful test, just checking)
		# get a job back from the test db
		_job = Job.Job.find_by_id(987654321, self.jobs)
		
		assert _job is not None
		assert _job.id == 987654321
		assert _job.owner is None
		
class JobPersistenceTestCaseUser(unittest.TestCase):
	def setUp(self):
		# set up the db
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.jobs = self.db.jobs
		
		# add a job
		# (make sure it has a .owner)
		self.test_job = Job.Job()
		self.test_job.id = 'test_JobPersistenceTestCaseUser_identifier'
		self.test_job.owner = 'test_JobPersistenceTestCaseUser_owner'
		self.test_job.status = 'test_JobPersistenceTestCaseUser_status'
		
		self.jobs.insert_one({'identifier':self.test_job.id, 'owner':self.test_job.owner, 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		
	def tearDown(self):
		# remove the job from the db
		self.jobs.delete_many({'identifier':self.test_job.id})

	def test_find_job_by_user(self):
		res = Job.Job.find_by_user_id(self.test_job.owner, self.jobs)
		
		assert res.owner == self.test_job.owner
		
	def test_find_job_by_user_missing_user_id(self):
		res = Job.Job.find_by_user_id(None, self.jobs)
		
		assert res == None
		
	def test_find_job_by_user_missing_collection(self):
		res = Job.Job.find_by_user_id(self.test_job.owner, None)
		
		assert res == None
		
class JobPersistenceTestCaseJob(unittest.TestCase):
	def setUp(self):
		# set up the db
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.jobs = self.db.jobs
		
		# add a job
		# (make sure it has a .identifier)
		self.test_job = Job.Job()
		self.test_job.id = 'test_JobPersistenceTestCaseJob_identifier'
		self.test_job.owner = 'test_JobPersistenceTestCaseJob_owner'
		self.test_job.status = 'test_JobPersistenceTestCaseJob_status'
		
		self.jobs.insert_one({'identifier':self.test_job.id, 'owner':self.test_job.owner, 'status':self.test_job.status, 'simulator_parameters':self.test_job.simulator_parameters})
		
	def tearDown(self):
		# remove the job from the db
		self.jobs.delete_many({'identifier':self.test_job.id})

	def test_find_job_by_id(self):
		res = Job.Job.find_by_id(self.test_job.id, self.jobs)
		
		assert res.id == self.test_job.id
		
	def test_find_job_by_user_missing_id(self):
		res = Job.Job.find_by_id(None, self.jobs)
		
		assert res == None

	def test_find_job_by_user_missing_collection(self):
		res = Job.Job.find_by_id(self.test_job.owner, None)
		
		assert res == None


if __name__ == '__main__':
	unittest.main()
