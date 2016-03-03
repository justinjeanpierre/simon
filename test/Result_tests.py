#!/usr/bin/python

import os	
import unittest
import simon

class ResultTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
		
	def tearDown(self):
		# destroy test db
		pass
			
	def test_store_result(self):
		pass
		
	def test_retrieve_result(self):
		pass
		
	def test_update_result(self):
		pass
		
	def test_delete_result(self):
		pass
		

if __name__ == '__main__':
	unittest.main()

