#!/usr/bin/python

import SimulatorParameters
from flask.ext.pymongo import PyMongo
from flask import g

import requests

class Job:
	def __init__(self):
		self.id = None # string
		self.owner = None # string
		self.status = None # some custom enum-like type?
		self.simulator_parameters = SimulatorParameters.SimulatorParameters().defaultParametersDictionary()
		
	def update(self, dict):
		# add params from user's input
		# (will accept dictionary of parameters)
		
		# parse supplied values
		for key in dict.keys():
			for k in self.simulator_parameters:
				if k == key:
					# (validate first, maybe?)
					self.simulator_parameters[k] = dict[key]
		
	def submit(self):
		req = requests.post('http://104.200.30.65/', data = {'simulator_parameters':self.simulator_parameters}) # callback or completion handler?
		
	def cancel(self):
		# just delete it from the database
		# controller route method will tell simulator
		pass

	def save(self, mongoCollection = None):
		# (should check db to see if this job exists first)
		return mongoCollection.insert_one({'identifier':self.id, 'owner':self.owner, 'status':self.status, 'simulator_parameters':self.simulator_parameters})
		
	@classmethod
	def find_by_id(_class, job_id, user_id, mongoCollection = None):
		# this function returns an instance of Job 
		# if one was found in the db with a matching job_id
		#
		# (you should pass in a Mongo collction if you have one)
		
		if user_id == None:
			return None
		
		if job_id == None:
			return None
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return None

		retval = None # empty Job to be returned later
		
		# this query needs to have the currently logged-in user's identifier
		# passed in as the owner, or else everyone's jobs will be returned
		res = mongoCollection.find_one({'identifier':job_id, 'owner':user_id}, {'_id':0}) # we don't need the object's _id
		if res is not None:
			tempJob = Job()
			
			try:
				tempJob.id = res['identifier']
			except:
				# maybe do something with the error?
				pass
						
			# try to load the other fields of db response into object:
			try:
				tempJob.owner = res['owner']
			except KeyError:
				pass

			try:
				tempJob.status = res['status']
			except:
				pass

			try:
				tempJob.simulator_parameters = res['simulator_parameters']
			except:
				pass
			retval = tempJob
		else:
			pass
		
		return retval
		
	@classmethod
	def find_by_user_id(_class, user_id, mongoCollection = None):
		# this is intended to return an array of Job objects
		# that belong to the currently logged-in user
				
		if user_id == None:
			return None
		
		if mongoCollection == None:
			return None
	
		# get all matching jobs (omit the parameters for now)
		res = mongoCollection.find({'owner':user_id}, {'_id':False, 'simulator_parameters': False})
		
		retval = []
		
		if res is not None:
			
			for d in list(res):
				j = Job()
				
				# only populate the object with db fields that exist
				try:
					j.id = d['identifier']
				except:
					pass
					
				try:
					j.owner = d['owner']
				except:
					pass
					
				try:
					j.status = d['status']
				except:
					pass
					
				try:
					j.simulator_parameters = d['simulator_parameters']
				except:
					pass
					
				retval.append(j)
		else:
			pass

		return retval
