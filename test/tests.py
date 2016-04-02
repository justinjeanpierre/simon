#!/usr/bin/python

import unittest

# imports from project
from JobsRouteTests import JobsRouteTestCase
from ResultsRouteTests import ResultsRoutesTestCase
from DocumentationRouteTests import DocumentationRoutesTestCase
from StatisticsRouteTests import StatsRoutesTestCase
from JobTests import JobTestCase
from ResultTests import ResultTestCase
from SimulatorParametersTest import SimulatorParametersTestCase
from PersistenceJobTests import JobPersistenceTestCase, JobPersistenceTestCaseJob, JobPersistenceTestCaseUser
from PersistenceResultTests import ResultPersistenceTestCase, ResultPersistenceTestCaseResult, ResultPersistenceTestCaseUser

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
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCaseJob))
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCaseUser))

	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCase))
	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCaseResult))
	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCaseUser))
		
	return test_suite

runner = unittest.TextTestRunner()
runner.run(test_suite())
