#!/usr/bin/python

import unittest

# imports from project
from JobsRouteTests import JobsRouteTestCase, JobsRouteTestCaseGET, JobsRouteTestCasePOST
from ResultsRouteTests import ResultsRoutesTestCase, ResultsRoutesTestCaseGET, ResultsRoutesTestCasePOST
from DocumentationRouteTests import DocumentationRoutesTestCase
from StatisticsRouteTests import StatsRoutesTestCase
from JobTests import JobTestCase
from ResultTests import ResultTestCase
from SimulatorParametersTest import SimulatorParametersTestCase
from PersistenceJobTests import JobPersistenceTestCase, JobPersistenceTestCaseJob, JobPersistenceTestCaseUser
from PersistenceResultTests import ResultPersistenceTestCase, ResultPersistenceTestCaseResult, ResultPersistenceTestCaseUser

def test_suite():
	test_suite = unittest.TestSuite()
	
	# Job routes (/jobs)
	test_suite.addTest(unittest.makeSuite(JobsRouteTestCase))
	test_suite.addTest(unittest.makeSuite(JobsRouteTestCaseGET))
	test_suite.addTest(unittest.makeSuite(JobsRouteTestCasePOST))

	# Result routes (/results)
	test_suite.addTest(unittest.makeSuite(ResultsRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(ResultsRoutesTestCaseGET))
	test_suite.addTest(unittest.makeSuite(ResultsRoutesTestCasePOST))

	test_suite.addTest(unittest.makeSuite(DocumentationRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(StatsRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(JobTestCase))
	test_suite.addTest(unittest.makeSuite(ResultTestCase))
	test_suite.addTest(unittest.makeSuite(SimulatorParametersTestCase))

	# db tests - Job
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCase))
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCaseJob))
	test_suite.addTest(unittest.makeSuite(JobPersistenceTestCaseUser))

	# db tests - Result
	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCase))
	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCaseResult))
	test_suite.addTest(unittest.makeSuite(ResultPersistenceTestCaseUser))
		
	return test_suite

runner = unittest.TextTestRunner()
runner.run(test_suite())
