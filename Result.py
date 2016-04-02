#!/usr/bin/python

class Result:
	def __init__(self):
		self.id = None # string?
		self.owner = None # the corresponding job for this set of results
		self.status = None # some custom enum-ish type ?
		self.parameters = {} # an empty dictionary
		
	# should be called when Simulator returns results
	def save(self, mongoCollection = None):
		# (should check db to see if this Result exists first)
		return mongoCollection.insert_one({'identifier':self.id, 'owner':self.owner, 'status':self.status, 'result_parameters':self.parameters})
		
	@classmethod
	def find_by_id(_class, result_id, mongoCollection = None):
		# this function returns an instance of Result if
		# one was found in the db with a matching result_id
		#
		# (you should pass in a Mongo collection if you have one)
		
		if result_id == None:
			return None
				
		if mongoCollection == None:
			return None

		retval = Result() # empty Result to be returned later

		res = mongoCollection.find_one({'identifier':result_id}, {'_id':0})
		if res is not None:
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
				retval.parameters = res['result_parameters']
			except:
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
			
		retval = Result()

		res = mongoCollection.find_one({'owner':user_id}, {'_id':0})
		# this query should not be find_one, we
		# are looking for ALL of a user's results.
		
		if res is not None:
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
				retval.parameters = res['parameters']
			except:
				pass

		return retval
