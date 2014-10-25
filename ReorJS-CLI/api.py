"""
	api.py
	Simple ReorJS API connector
	
	--
	Provides simple programmatic access to the ReorJS server API calls for managing
	ReorJS application, dataset and task objects
	--
	
	Author(s) 	- Philip Skinner (philip@crowdca.lc)
	Last modified 	- 2014-08-24
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	    
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	         
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
	Copyright (c) 2014, Crowdcalc B.V.
"""

import urllib
import urllib2
import httplib2
import simplejson as json

class API():
	def __init__(self):
		self.host = 'http://localhost:9999' #default
		self.key = ''
	
	def setHost(self, host):
		self.host = host
	
	def setKey(self, key):
		self.key = key
		
	def connectionTest(self):
		#simply connect to the server
		try:
			response = urllib2.urlopen(self.host + '/output/v1/ping?key=%s' % self.key)

			if response.getcode() == 200:
				return True
		except:
			pass
		
		return False
	
	def checkData(self, data):
		if 'meta' in data:
			if 'code' in data['meta']:
				if str(data['meta']['code']) == '200':
					if 'data' in data:
						return data['data']
					elif 'status' in data:
						return data
				else:
					if 'error' in data:
						return { 'error' : data['error'], 'code' : data['meta']['code'] }
		return []

	def detailTask(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/task/%s?key=%s' % (id, self.key))
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return {}
	
	def createTask(self, application=None, dataset=None, result=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/task'                      
			body = urllib.urlencode({
				'application' : application,
				'dataset' : dataset,
				'result' : result,
				'key' : self.key,
			}) 
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
			
		return {}

	def listTasks(self):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/task?key=%s' % (self.key))
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return []

	def createDataset(self, name=None, source_type=None, source_hostname=None, source_port=None, source_name=None, source_table=None, source_username=None, source_password=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/dataset'                       
			
			body = urllib.urlencode({
				'name'			: name,
				'source_type' 		: source_type,
				'source_hostname' 	: source_hostname,
				'source_port' 		: source_port,
				'source_name' 		: source_name,
				'source_table' 		: source_table,
				'source_username' 	: source_username,
				'source_password' 	: source_password,	
				'key'			: self.key,
			})
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
		
		return {}

	def modifyDataset(self, id=None, name=None, source_type=None, source_hostname=None, source_port=None, source_name=None, source_table=None, source_username=None, source_password=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/dataset/%s' % id
			
			body = urllib.urlencode({
				'name'			: name,
				'source_type' 		: source_type,
				'source_hostname' 	: source_hostname,
				'source_port' 		: source_port,
				'source_name' 		: source_name,
				'source_table' 		: source_table,
				'source_username' 	: source_username,
				'source_password' 	: source_password,	
				'key'			: self.key,
			})
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
		
		return {}

	def deleteDataset(self, id=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/dataset/%s?key=%s' % (id, self.key)
			response, content = connection.request(url, method='DELETE', headers={}, body='')
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
		
		return {}

	def detailDataset(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/dataset/%s?key=%s' % (id, self.key))
			
			if response.getcode() == 200:
				raw = response.read()					
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return {}
	
	def listDatasets(self):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/dataset?key=%s' % (self.key))
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
		
		return []
	
	def createApplication(self, name=None, program=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/application'                       
			
			body = urllib.urlencode({
				'name'		: name,
				'program'	: program,
				'key'		: self.key,
			})
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)			
		except:
			pass
		
		return {}
		
	def modifyApplication(self, id=None, name=None, program=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application/%s' % id
			
			body = urllib.urlencode({
				'name'		: name,
				'program'	: program,
				'key'		: self.key,
			})

			response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
			
		return {}

	def deleteApplication(self, id=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application/%s?key=%s' % (id, self.key)
			
			response, content = connection.request(url, method='DELETE', headers={}, body='')
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
			
		return {}

	def detailApplication(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/application/%s?key=%s' % (id, self.key))
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return {}

	def listApplications(self):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/application?key=%s' % self.key)
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return []
	
	def ping(self):
		try:
			response = urllib2.urlopen(self.host + '/output/v1/ping?key=%s' % self.key)
			
			if response.getcode() == 200:
				raw = response.read()

				data = { 'error' : 'Could not reach output service', 'code' : '9002' }

				if raw == 'PONG':
					data = { 'status' : { 'message' : 'PONG received!' }, 'code' : '200' }
					
				return data
		except:
			pass
		
		return {}

	def status(self):
		try:
			response = urllib2.urlopen(self.host + '/output/v1/status?key=%s' % self.key)
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
		
		return {}
