#!/usr/bin/python

class Result:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # the corresponding job for this set of results
		self.status = "" # some type ?
		self.parameters = {}
				
	def save(self, mongoCollection = None):
		# (should check db to see if this Result exists first)
		return mongoCollection.insert_one({'identifier':self.id, 'result_parameters':self.parameters})
		
	@classmethod
	def find_by_id(_class, result_id, mongoCollection = None):
		# this function returns an instance of Result 
		# if one was found in the db with a matching result_id
		#
		# (you should pass in a Mongo collction if you have one)
		
		retval = Result() # empty Result to be returned later
		
		if mongoCollection == None:
			# maybe handle this situation a bit better..?
			return retval

		res = mongoCollection.find_one({'identifier':result_id})
		if res is not None:
			retval.id = res['identifier']
			# validate then uncomment this
#			retval.parameters = res['result_parameters']
		
		return retval
