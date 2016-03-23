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
		
	def tearDown(self):
		# remove test data from test db
		self.results.delete_many({'identifier':'test_result_identifier'})
		self.results.delete_many({'identifier':987654321})
		self.results.delete_many({'identifier':self.test_store_result_identifier})
		
	def test_retrieve_result(self):
		# get a result back from the test db
		_result = Result.Result.find_by_id(987654321, self.results)
		
		assert _result is not None
		assert _result.id == 987654321
		
	def test_store_result(self):
		_result = Result.Result()
		
		# reassurance
		assert _result is not None
		assert _result.id == ''
		assert _result.owner == ''
		assert _result.status == ''
		
		# save the Result
		_result.id = self.test_store_result_identifier
		_result.save(self.results)
		
		# create an "empty" Result
		saved_result = Result.Result()
		
		# populate the empty Result with db data
		res = self.results.find_one({'identifier':_result.id}) 
		if res is not None:
			saved_result.id = res['identifier']
			saved_result.parameters = res['result_parameters']
		
		# compare db data with test Result
		assert saved_result is not None
		assert saved_result.id == self.test_store_result_identifier
		assert saved_result.parameters == _result.parameters


if __name__ == '__main__':
	unittest.main()
