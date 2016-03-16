#!/usr/bin/python

import os	
import unittest
import simon

class JobsRouteTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
	def test_get_jobs(self):
		response = self.app.get('/jobs')
		
		assert response.status == '501 NOT IMPLEMENTED'

	def test_get_job(self):
		response = self.app.get('/jobs/123')
		
		assert response.status == '501 NOT IMPLEMENTED'

	def test_post_job(self):
		response = self.app.post('/jobs/234')
		
		assert response.status == '501 NOT IMPLEMENTED'

	def test_put_job(self):
		response = self.app.put('/jobs/345')
		
		assert response.status == '501 NOT IMPLEMENTED'

	def test_delete_job(self):
		response = self.app.delete('/jobs/567')
		
		assert response.status == '501 NOT IMPLEMENTED'

if __name__ == '__main__':
	unittest.main()
