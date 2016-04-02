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
		
		retval = Result() # empty Result to be returned later
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return retval

		res = mongoCollection.find_one({'identifier':result_id})
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
		retval = Result()
		
		if mongoCollection == None:
			return retval
			
		res = mongoCollection.find_one({'owner':user_id})
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