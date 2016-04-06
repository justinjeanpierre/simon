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
		self.test_result.owner = 'test_RESULTS_ROUTE_TESTS_owner'
		self.test_result.status = 'test_RESULTS_ROUTE_TESTS_status'
		
		self.results.insert_one({'identifier':str(1001), 'owner':self.test_result.owner, 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		self.results.insert_one({'identifier':str(1002), 'owner':str(115122217971165854689), 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		self.results.insert_one({'identifier':str(1003), 'owner':str(115122217971165854689), 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		self.results.insert_one({'identifier':str(1004), 'owner':str(2593451828), 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		self.results.insert_one({'identifier':str(1005), 'owner':str(2593451828), 'status':self.test_result.status, 'parameters':self.test_result.parameters})
		self.results.insert_one({'identifier':str(1006), 'owner':str(2593451828), 'status':self.test_result.status, 'parameters':self.test_result.parameters})

	def tearDown(self):
		# remove test data from test db
		self.results.delete_many({'identifier':self.test_result.id})
		self.results.delete_many({'owner':'test_RESULTS_ROUTE_TESTS_owner'})
		self.results.delete_many({'owner':str(115122217971165854689)})
		self.results.delete_many({'owner':str(2593451828)})

	def test_get_result(self):
		response = self.app.get('/results/1000')
		
		assert response.status == '401 UNAUTHORIZED'

	def test_get_results(self):
		response = self.app.get('/results')
		
		assert response.status == '401 UNAUTHORIZED'
	

class ResultsRoutesTestCasePOST(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()

	def tearDown(self):
		pass

#	def test_post_results(self):
#		d = dict(maximum_frequency=1000)
#		response = self.app.post('/results', data=d)
#		
#		assert response.status == '200 OK'


if __name__ == '__main__':
	unittest.main()
