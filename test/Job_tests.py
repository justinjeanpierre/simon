#!/usr/bin/python

import os	
import unittest
import simon

class JobTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
		
	def tearDown(self):
		# destroy test db
		pass
			
	def test_store_job(self):
		pass
		
	def test_retrieve_job(self):
		pass
		
	def test_update_job(self):
		pass
		
	def test_delete_job(self):
		pass
		

if __name__ == '__main__':
	unittest.main()

