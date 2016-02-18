#!/usr/bin/python

import os	
import unittest
from src import simon

class NewTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
#	def tearDown(self):
#		nothing to tear down yet.
		
	def test_get_route(self):
		response = self.app.get('/users')
		assert 'this is a response to a GET request to /users' in response.data
		
	def test_post_route(self):
		response = self.app.post('/users')
		assert 'this is a response to a POST request to /users' in response.data
		
	def test_put_route(self):
		response = self.app.put('/users')
		assert 'this is a response to a PUT request to /users' in response.data

if __name__ == '__main__':
	unittest.main()
