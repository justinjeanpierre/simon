#!/usr/bin/python

import os	
import unittest
import simon

class StatsRoutesTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
	def test_get_stats(self):
		response = self.app.get('/stats')
		assert response.status == '501 NOT IMPLEMENTED'
		

if __name__ == '__main__':
	unittest.main()
