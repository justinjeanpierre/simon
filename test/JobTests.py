#!/usr/bin/python

import os	
import unittest
import Job
import SimulatorParameters

class JobTestCase(unittest.TestCase):
		
	def setUp(self):
		self.job = Job.Job()
		
	def tearDown(self):
		# destroy test db
		pass
		
#	def test_default_params(self):
#		d = self.job.simulator_parameters
#
#		assert d['GENERAL_OUTPUT_FILE'] == 'sim.out'
#		assert d['GENERAL_TOTAL_CORES'] == 64
#		assert d['GENERAL_ENABLE_MODELING_CORE'] == True
					
	def test_empty_param_handling(self):
		# should evaluate what we do with keys that are not found
		# or have values that are None or nil or empty
		pass
				

if __name__ == '__main__':
	unittest.main()

