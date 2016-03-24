#!/usr/bin/python

import plistlib

class SimulatorParameters:
	def __init__(self):
		self.simulator_parameters = {}
		
	def defaultParametersDictionary(self):
		path = 'data/default_simulator_parameters.plist'
		data_file = plistlib.readPlist(path)
		self.simulator_parameters = data_file[0]

		return data_file[0]
