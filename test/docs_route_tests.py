#!/usr/bin/python

import os	
import unittest
import simon

class DocumentationRoutesTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
	def test_get_docs(self):
		response = self.app.get('/docs')

		assert response.status == '501 NOT IMPLEMENTED'
		

if __name__ == '__main__':
	unittest.main()

