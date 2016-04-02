#!/usr/bin/python

import SimulatorParameters
from flask.ext.pymongo import PyMongo

class Job:
	def __init__(self):
		self.id = None # string
		self.owner = None # string
		self.status = None # some custom enum-like type?
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
		return mongoCollection.insert_one({'identifier':self.id, 'owner':self.owner, 'status':self.status, 'simulator_parameters':self.simulator_parameters})
		
	@classmethod
	def find_by_id(_class, job_id, mongoCollection = None):
		# this function returns an instance of Job 
		# if one was found in the db with a matching job_id
		#
		# (you should pass in a Mongo collction if you have one)
		
		if job_id == None:
			return None
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return None

		retval = Job() # empty Job to be returned later
		
		# this query needs to have the currently logged-in user's identifier
		# passed in as the owner, or else everyone's jobs will be returned
		res = mongoCollection.find_one({'identifier':job_id}, {'_id':0}) # we don't need the object's _id
		if res is not None:
			try:
				retval.id = res['identifier']
			except:
				# maybe do something with the error?
				pass
						
			# try to load the other fields of db response into object:
			try:
				retval.owner = res['owner']
			except KeyError:
				pass

			try:
				retval.status = res['status']
			except:
				pass

			try:
				retval.simulator_parameters = res['simulator_parameters']
			except:
				pass
		else:
			pass
		
		return retval
		
	@classmethod
	def find_by_user_id(_class, user_id, mongoCollection = None):
		# this is intended to return all Jobs that belong
		# to a specific (i.e.: currently logged-in) user
				
		if user_id == None:
			return None
		
		if mongoCollection == None:
			return None
		
		retval = Job()
	
		res = mongoCollection.find_one({'owner':user_id}, {'_id':0})
		if res is not None:
			# only populate the object with db fields that exist
			try:
				retval.id = res['identifier']
			except:
				pass
				
			try:
				retval.owner = res['owner']
			except:
				pass
				
			try:
				retval.status = res['status']
			except:
				pass
				
			try:
				retval.simulator_parameters = res['simulator_parameters']
			except:
				pass
		else:
			pass

		return retval
