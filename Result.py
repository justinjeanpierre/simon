#!/usr/bin/python

import requests

class Result:
	def __init__(self):
		self.id = None # string?
		self.owner = None # the corresponding job for this set of results
		self.status = None # some custom enum-ish type ?
		self.parameters = {} # an empty dictionary
		
	def update(self, dict):
		for key in dict.keys():
			for k in self.parameters:
				if k == key:
					#figure out types (num -> num, string -> string, etc.)
					# (validate first, maybe?)
					self.parameters[k] = dict[key]
		
	# should be called when Simulator returns results
	def save(self, mongoCollection = None):
		# (should check db to see if this Result exists first)
		val = mongoCollection.insert_one({'identifier':self.id, 'owner':self.owner, 'status':self.status, 'result_parameters':self.parameters})
		
		# get the newly-created object's _id
		object_id_str = str(val.inserted_id)

		# get the last 8 characters of the object id
		new_id = object_id_str[len(object_id_str)-8:]

		# update 'identifier' field with new_id
		mongoCollection.update_one({'_id':val.inserted_id}, {'$set':{'identifier':new_id}}, upsert=False)
		
		return new_id
	
	@classmethod
	def find_by_id(_class, result_id, user_id, mongoCollection = None):
		# this function returns an instance of Result if
		# one was found in the db with a matching result_id
		#
		# (you should pass in a Mongo collection if you have one)
		
		if user_id == None:
			return None
		
		if result_id == None:
			return None
				
		if mongoCollection == None:
			return None

		retval = None # empty Result to be returned later

		res = mongoCollection.find_one({'identifier':result_id, 'owner':user_id}, {'_id':0})
		if res is not None:
			tempResult = Result()
			
			try:
				tempResult.id = res['identifier']
			except:
				pass

			try:
				tempResult.owner = res['owner']
			except:
				pass

			try:
				tempResult.status = res['status']
			except:
				pass
	
			try:
				tempResult.parameters = res['result_parameters']
			except:
				pass
			
			retval = tempResult
		else:
			pass
			
		return retval

	@classmethod
	def find_by_user_id(_class, user_id, mongoCollection = None):
		# this is intended to return all Results that belong
		# to a specific (i.e.: currently logged-in) user
		
		if user_id == None:
			return None
		
		if mongoCollection == None:
			return None
			
		res = mongoCollection.find({'owner':user_id}, {'_id':0, 'result_parameters': 0})
		# this query should not be find_one, we
		# are looking for ALL of a user's results.
		
		retval = []

		if res is not None:

			for d in list(res):
				r = Result()
				
				try:
					r.id = d['identifier']
				except:
					pass
				
				try:
					r.owner = d['owner']
				except:
					pass
				
				try:
					r.status = d['status']
				except:
					pass
				
				try:
					r.parameters = d['result_parameters']
				except:
					pass
			
				retval.append(r)
		else:
			pass
			
		return retval
