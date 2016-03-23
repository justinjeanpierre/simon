#!/usr/bin/python

import os	
import unittest
import SimulatorParameters

class SimulatorParametersTestCase(unittest.TestCase):
		
	def setUp(self):
		pass
							
	def test_load_default_params(self):
		d = SimulatorParameters.SimulatorParameters().defaultParametersDictionary()

		assert d != None
		assert d['GENERAL_OUTPUT_FILE'] == 'sim.out'


if __name__ == '__main__':
	unittest.main()
