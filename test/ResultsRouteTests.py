#!/usr/bin/python

import os	
import unittest
import simon

class ResultsRoutesTestCase(unittest.TestCase):
		
	def setUp(self):
		pass
			
	def tearDown(self):
		pass
		
		
class ResultsRoutesTestCaseGET(unittest.TestCase):
	def setUp(self):
		self.app = simon.app.test_client()

	def tearDown(self):
		pass

	def test_get_results(self):
		response = self.app.get('/results')
		
		assert response.status == '200 OK'
		
	def test_get_result(self):
		response = self.app.get('/results/987')
		
		assert response.status == '501 NOT IMPLEMENTED'


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
