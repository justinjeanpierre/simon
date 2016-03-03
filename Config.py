#!/usr/bin/python

from flask.ext.pymongo import PyMongo

class Config(object):
	def __init__(self):
		pass

class ProductionConfig(Config):
	# production db
	MONGO_DBNAME = 'simon'

class DevelopmentConfig(Config):
	# dev db
	MONGO_DBNAME = 'simon_dev'
