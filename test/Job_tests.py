#!/usr/bin/python

import os	
import unittest
import simon
import Job

class JobTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
		self.job = Job.Job()
		
	def tearDown(self):
		# destroy test db
		pass
					
	def test_store_job(self):
		# store a job in the db
		pass
		
	def test_retrieve_job(self):
		# get a job back from the test/dev db
		pass
		
	def test_empty_param_handling(self):
		# should evaluate what we do with keys that are not found
		# or have values that are None or nil or empty
		pass
		
	def test_update_job(self):
		# validate parameters
#		self.job.update({'TOTAL_CORES':12})
#		assert self.job.simulator_parameters['TOTAL_CORES'] == 12
#		self.job.update({'TOTAL_CORES'})
#		assert self.job.simulator_parameters['TOTAL_CORES'] == None
		
	def test_delete_job(self):
		pass
		

if __name__ == '__main__':
	unittest.main()

