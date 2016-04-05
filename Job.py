#!/usr/bin/python

import SimulatorParameters
from flask.ext.pymongo import PyMongo
from flask import g

class Job:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # string
		self.status = "" # ?type?
		self.simulator_parameters = SimulatorParameters.SimulatorParameters().defaultParametersDictionary()
		
	def update(self, dict):
		# add params from user's input
		# (will accept dictionary of parameters)
		
		# load supplied values

		for key in dict.keys():
			for k in self.simulator_parameters:
				if k == key:
					#figure out types (num -> num, string -> string, etc.)
					# (validate first, maybe?)
					self.simulator_parameters[k] = dict[key]
		
	def submit(self):
		# save user input
		# send to simulator
		pass
		
	def cancel(self):
		# just delete it from the database
		# controller route method will tell simulator
		pass

	def save(self, mongoCollection = None):
		# (should check db to see if this job exists first)
		return mongoCollection.insert_one({'identifier':self.id, 'simulator_parameters':self.simulator_parameters})
		
	@classmethod
	def find_by_id(_class, job_id, mongoCollection = None):
		# this function returns an instance of Job 
		# if one was found in the db with a matching job_id
		#
		# (you should pass in a Mongo collction if you have one)
		
		retval = Job() # empty Job to be returned later
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return retval

		res = mongoCollection.find_one({'identifier':job_id})
		if res is not None:
			retval.id = res['identifier']
			# validate then uncomment this
#			retval.simulator_parameters = res['simulator_parameters']
		
		return retval
