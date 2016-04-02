#!/usr/bin/python

import os	
import unittest

from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from Config import TestingConfig

import simon
import Result

class ResultsRoutesTestCase(unittest.TestCase):
		
	def setUp(self):
		pass
			
	def tearDown(self):
		pass
		
		
class ResultsRoutesTestCaseGET(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()

		# initialization stuff
		# make sure mongod is running first!!!
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[TestingConfig.MONGO_DBNAME]
		self.results = self.db.results
		
		self.test_result = Result.Result()
		self.test_result.id = str(514514)
		self.test_result.owner = 'test_RESULTS_ROUTE_TESTS_owner'
		self.test_result.status = 'test_RESULTS_ROUTE_TESTS_status'
		
		self.results.insert_one({'identifier':self.test_result.id, 'owner':self.test_result.owner, 'status':self.test_result.status, 'parameters':self.test_result.parameters})

	def tearDown(self):
		# remove test data from test db
		self.results.delete_many({'identifier':self.test_result.id})
		pass

	def test_get_results(self):
		response = self.app.get('/results')
		
		assert response.status == '200 OK'
		
	def test_get_result(self):
		response = self.app.get('/results/514514')
		
		assert '514514' in response.data
		
		assert response.status == '200 OK'


class ResultsRoutesTestCasePOST(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()

	def tearDown(self):
		pass

	def test_post_results(self):
		response = self.app.post('/results')
		
		assert response.status == '501 NOT IMPLEMENTED'
		
		assert response.status == '501 NOT IMPLEMENTED'


if __name__ == '__main__':
	unittest.main()
