#!/usr/bin/python

class Result:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # the corresponding job for this set of results
		self.status = "" # some type ?

	def create(self):
		# triggered by response from simulator
		# user should not be able to create a Result
		pass
		
	def delete(self):
		# delete from records (triggered by user)
		pass
