#!/usr/bin/python

import os	
import unittest
from src import simon

class NewTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
		print "set up complete"
					
	def test_one(self):
		response = self.app.get('/jobs')
		assert 'this is a response to a GET request' in response.data

if __name__ == '__main__':
	unittest.main()
