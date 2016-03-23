#!/usr/bin/python

# imports
import unittest

# imports from project
from JobsRouteTests import JobsRouteTestCase
from ResultsRouteTests import ResultsRoutesTestCase
from DocumentationRouteTests import DocumentationRoutesTestCase
from StatisticsRouteTests import StatsRoutesTestCase
from JobTests import JobTestCase
from ResultTests import ResultTestCase
from SimulatorParametersTest import SimulatorParametersTestCase
from PersistenceJobTests import JobPersistenceTestCase

def test_suite():
	test_suite = unittest.TestSuite()
	
	test_suite.addTest(unittest.makeSuite(JobsRouteTestCase))
	test_suite.addTest(unittest.makeSuite(ResultsRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(DocumentationRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(StatsRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(JobTestCase))
	test_suite.addTest(unittest.makeSuite(ResultTestCase))
	test_suite.addTest(unittest.makeSuite(SimulatorParametersTestCase))
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCase))
	
	return test_suite

runner=unittest.TextTestRunner()
runner.run(test_suite())
