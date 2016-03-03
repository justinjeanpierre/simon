#!/usr/bin/python

class Job:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # string
		self.status = "" # ?type?
		
	def update(self):
		# add params from user's input
		pass
		
	def submit(self):
		# save user input and send to simulator
		pass
		
	def cancel(self):
		# cancel simulation (if in progress)
		# and delete it from the database
		pass
