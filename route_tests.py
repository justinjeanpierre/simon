#!/usr/bin/python
import os
import unittest
import simon

class SimonTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = simon.app.test_client()
				
	def test_get_route(self):
		response = self.app.get('/jobs')
		assert 'this is a response to a GET request' in response.data
		
	def test_post_route(self):
		response = self.app.post('/jobs')
		assert 'this is a response to a POST request' in response.data
		
	def test_put_route(self):
		response = self.app.put('/jobs')
		assert 'this is a response to a PUT request' in response.data
		
if __name__ == '__main__':
	unittest.main()
