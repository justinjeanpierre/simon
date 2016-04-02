#!/usr/bin/python

import os	
import unittest
from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig
import json

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
	def test_find_result_by_user(self):
		assert False
		
class ResultPersistenceTestCaseResult(unittest.TestCase):
	def test_find_result_by_id(self):
		assert False
		
		
if __name__ == '__main__':
	unittest.main()
