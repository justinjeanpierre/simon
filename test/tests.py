#!/usr/bin/python

# imports
import unittest

# imports from project
from jobs_route_tests import JobsRouteTestCase
from results_route_tests import ResultsRoutesTestCase
from docs_route_tests import DocumentationRoutesTestCase
from stats_route_tests import StatsRoutesTestCase

def test_suite():
	test_suite = unittest.TestSuite()
	
	test_suite.addTest(unittest.makeSuite(JobsRouteTestCase))
	test_suite.addTest(unittest.makeSuite(ResultsRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(DocumentationRoutesTestCase))
	test_suite.addTest(unittest.makeSuite(StatsRoutesTestCase))
	
	return test_suite

runner=unittest.TextTestRunner()
runner.run(test_suite())
