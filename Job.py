#!/usr/bin/python

import SimulatorParameters
from flask.ext.pymongo import PyMongo

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
		
		# load supplied values

		for key in keys:
			for k in self.simulator_parameters:
				if k == key:
					#figure out types (num -> num, string -> string, etc.)
					# (validate first, maybe?)
					self.simulator_parameters[k] = dict[key]
		
	def submit(self):
		# save user input and send to simulator
		pass
		
	def cancel(self):
		# cancel simulation (if in progress)
		# and delete it from the database
		pass

	@classmethod
	def find_job(_class, job_id, mongoCollection = None):
		# this function returns an instance of Job 
		# if one was found in the db with a matching job_id
		#
		# (you should pass in a Mongo collction if you have one)
		
		retval = _class() # empty Job to be returned later
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return retval

		res = mongoCollection.find_one({'identifier':job_id})
		if res is not None:
			retval.id = res['identifier']
		
		return retval
