#!/usr/bin/python

import os	
import unittest
import simon

class JobsRouteTestCase(unittest.TestCase):
		
	def setUp(self):
		self.app = simon.app.test_client()
			
	def test_get_jobs(self):
		response = self.app.get('/jobs')
		
		assert 'this is a response to a GET request' in response.data
		assert response.status == '200 OK'

	def test_get_job(self):
		response = self.app.get('/jobs/123')
		
		assert '123' in response.data
		assert response.status == '200 OK'

	def test_post_job(self):
		response = self.app.post('/jobs/234')
		
		assert 'this is a response to a POST request' in response.data
		assert response.status == '200 OK'

	def test_put_job(self):
		response = self.app.put('/jobs/345')
		
		assert 'this is a response to a PUT request' in response.data
		assert response.status == '200 OK'

	def test_delete_job(self):
		response = self.app.delete('/jobs/567')
		
		assert 'this is a response to a DELETE request' in response.data
		assert response.status == '200 OK'


if __name__ == '__main__':
	unittest.main()
