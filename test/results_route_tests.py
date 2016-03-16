#!/usr/bin/python

import os	
import unittest
import simon

class ResultsRoutesTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
	def test_get_results(self):
		response = self.app.get('/results')
		
		assert response.status == '501 NOT IMPLEMENTED'
		
	def test_get_result(self):
		response = self.app.get('/results/987')
		
		assert response.status == '501 NOT IMPLEMENTED'


if __name__ == '__main__':
	unittest.main()
