#!/usr/bin/python

import os	
import unittest
import Job

class PersistenceTestCase(unittest.TestCase):
		
	def setUp(self):
		# configure the db
		pass
		
	def tearDown(self):
		# destroy test db
		pass
		
	def test_store_job(self):
		# store a job in the db
		pass
		
	def test_retrieve_job(self):
		# get a job back from the test db
		pass
		
	def test_delete_job(self):
		# delete a job from the test db
		pass
		

if __name__ == '__main__':
	unittest.main()
