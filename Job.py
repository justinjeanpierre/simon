#!/usr/bin/python

import SimulatorParameters

class Job:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # string
		self.status = "" # ?type?
		self.simulator_parameters = SimulatorParameters.SimulatorParameters().defaultParametersDictionary()
		
	def update(self, dict):
		# add params from user's input
		# (will accept dictionary of parameters)
		keys = dict.keys()
		print keys

	def submit(self):
		# save user input and send to simulator
		pass
		
	def cancel(self):
		# cancel simulation (if in progress)
		# and delete it from the database
		pass
