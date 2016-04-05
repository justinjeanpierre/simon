#!/usr/bin/python

import os	
import unittest
from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig

import simon
import Result

class ResultPersistenceTestCase(unittest.TestCase):
		
	def setUp(self):
		# initialization stuff
		# make sure mongod is running first!!!
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.results = self.db.results
		
		self.test_result = Result.Result()
		test_result = {'identifier':'test_result_identifier'}
		test_result = {'identifier':987654321}
		self.results.insert_one(test_result)

		# some available stuff
		self.test_store_result_identifier = 8765
		self.test_store_result_owner = 'SOME_RESULT_OWNER'
		self.test_store_result_status = 'SOME_RESULT_STATUS'
		
	def tearDown(self):
		# remove test data from test db
		self.results.delete_many({'identifier':'test_result_identifier'})
		self.results.delete_many({'identifier':987654321})
		self.results.delete_many({'identifier':self.test_store_result_identifier})
		
	def test_store_result(self):
		_result = Result.Result()
		
		# reassurance
		assert _result is not None
		assert _result.id is None
		assert _result.owner is None
		assert _result.status is None
		
		# populate properties with test data
		_result.id = self.test_store_result_identifier
		_result.owner = self.test_store_result_owner
		_result.status = self.test_store_result_status
		
		# tell the Result to save itself
		_result.save(self.results)
		
		# create an "empty" Result
		saved_result = Result.Result()
		
		# populate the empty Result with db data
		res = self.results.find_one({'identifier':_result.id}) 
		if res is not None:
			saved_result.id = res['identifier']
			saved_result.owner = res['owner']
			saved_result.status = res['status']
			saved_result.parameters = res['result_parameters']
		
		# compare db data with test Result
		assert saved_result is not None
		assert saved_result.id == self.test_store_result_identifier
		assert saved_result.owner == self.test_store_result_owner
		assert saved_result.status == self.test_store_result_status
		assert saved_result.parameters == _result.parameters

	def test_retrieve_result(self): #(not a useful test, just checking)
		# get a result back from the test db
		_result = Result.Result.find_by_id(987654321, self.results)

		assert _result is not None
		assert _result.id == 987654321
		assert _result.owner is None
		assert _result.status is None

class ResultPersistenceTestCaseUser(unittest.TestCase):
	def setUp(self):
		# set up db
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.results = self.db.results
		
		# put something in it
		self.test_result = Result.Result()
		self.test_result.id = 'test_ResultPersistenceTestCaseUser'
		self.test_result.owner = '_test_owner_id'
		self.test_result.status = 'test status'
		
		self.results.insert_one({'identifier':self.test_result.id, 'owner':self.test_result.owner, 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		
	def tearDown(self):
		# remove test Result from test db
		self.results.delete_many({'identifier':self.test_result.id})

	def test_find_result_by_user(self):
		res = Result.Result.find_by_user_id(self.test_result.owner, self.results)
		
		assert res.owner == self.test_result.owner
		
	def test_find_job_by_user_missing_user_id(self):
		res = Result.Result.find_by_user_id(None, self.results)

		assert res == None

	def test_find_job_by_user_missing_collection(self):
		res = Result.Result.find_by_user_id(self.results, None)

		assert res == None

class ResultPersistenceTestCaseResult(unittest.TestCase):
	def setUp(self):
		# configure db and connection
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.results = self.db.results
		
		# store a Result in the db
		self.test_result = Result.Result()
		self.test_result.id = 'test_ResultPersistenceTestCaseResult'
		self.test_result.owner = '_test_owner_id'
		self.test_result.status = 'a status'
		
		self.results.insert_one({'identifier':self.test_result.id, 'owner':self.test_result.owner, 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		
	def tearDown(self):
		# remove test Result from the test db
		self.results.delete_many({'identifier':self.test_result.id})

	def test_find_result_by_id(self):
		res = Result.Result.find_by_id(self.test_result.id, self.results)
		
		assert res.id == self.test_result.id
		
	def test_find_job_by_id_missing_user_id(self):
		res = Result.Result.find_by_id(None, self.results)

		assert res == None

	def test_find_job_by_id_missing_collection(self):
		res = Result.Result.find_by_id(self.results, None)

		assert res == None

if __name__ == '__main__':
	unittest.main()
