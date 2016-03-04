#!/usr/bin/python

class Job:
	def __init__(self):
		self.id = "" # string?
		self.owner = "" # string
		self.status = "" # ?type?
		self.simulator_parameters = {}
		
		# initialize simulator parameters to defaults
		self.simulator_parameters['TOTAL_CORES'] = None
		self.simulator_parameters['NUM_PROCESSES'] = None
		self.simulator_parameters['ENABLE_MODELING_CORE'] = None
		self.simulator_parameters['ENABLE_MODELING_POWER'] = None
		self.simulator_parameters['ENABLE_MODELING_AREA'] = None
		self.simulator_parameters['ENABLE_SHARED_MEM'] = None
		self.simulator_parameters['SIMULATOR_MODE'] = None
		self.simulator_parameters['TRIGGER_MODELS_WIN_APPLICATION'] = None
		self.simulator_parameters['TECHNOLOGY_NODE'] = None
		self.simulator_parameters['MAX_FREQUENCY'] = None
		self.simulator_parameters['TEMPERATURE'] = None
		self.simulator_parameters['TILE_WIDTH'] = None
		self.simulator_parameters['BASE_PORT'] = None
		
	def update(self, dict):
		# add params from user's input
		# (will accept parameter dictionary)
		keys = dict.keys()
		print keys
		
		print self.simulator_parameters['TOTAL_CORES']
		
#		if 'TOTAL_CORES' in keys:
#			self.simulator_parameters['TOTAL_CORES'] = dict['TOTAL_CORES']
#		else:
#			# what to do with key that is not in dict
#			pass
		
	def submit(self):
		# save user input and send to simulator
		pass
		
	def cancel(self):
		# cancel simulation (if in progress)
		# and delete it from the database
		pass
