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
			response = urllib2.urlopen(self.host + '/output/v1/ping')

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
		return None

	def detailTask(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/task/%s' % id)
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return None
	
	def createTask(self, application=None, dataset=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/task'                       
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body='application=%s&dataset=%s' % (application, dataset))
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
			
		return None

	def listTasks(self):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/task')
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return None

	def createDataset(self, name=None, source_type=None, source_hostname=None, source_port=None, source_name=None, source_table=None, source_username=None, source_password=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/dataset'                       
			
			body = 'name=%s' 		% name
			body += '&source_type=%s' 	% source_type
			body += '&source_hostname=%s' 	% source_hostname
			body += '&source_port=%s' 	% source_port
			body += '&source_name=%s' 	% source_name
			body += '&source_table=%s' 	% source_table
			body += '&source_username=%s' 	% source_username
			body += '&source_password=%s' 	% source_password
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
		
		return None

	def modifyDataset(self, id=None, name=None, source_type=None, source_hostname=None, source_port=None, source_name=None, source_table=None, source_username=None, source_password=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/dataset/%s' % id
			
			body = 'name=%s' 		% name
			body += '&source_type=%s' 	% source_type
			body += '&source_hostname=%s' 	% source_hostname
			body += '&source_port=%s' 	% source_port
			body += '&source_name=%s' 	% source_name
			body += '&source_table=%s' 	% source_table
			body += '&source_username=%s' 	% source_username
			body += '&source_password=%s' 	% source_password
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)
		except:
			pass
		
		return None

	def deleteDataset(self, id=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/dataset/%s' % id
			response, content = connection.request(url, method='DELETE', headers={}, body='')
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
		
		return None

	def detailDataset(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/dataset/%s' % id)						
			
			if response.getcode() == 200:
				raw = response.read()					
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return None
	
	def listDatasets(self):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/dataset')
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
		
		return None		
	
	def createApplication(self, name=None, program=None):
		try:
			connection = httplib2.Http()		       
			url = self.host + '/api/v1/application'                       
			
			body = 'name=%s' 	% name
			body += '&program=%s' 	% program
			
                        response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
                                
                        if response.status == 200:
                              	data = json.loads(content)
                               	return self.checkData(data)			
		except:
			pass
		
		return None
		
	def modifyApplication(self, id=None, name=None, program=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application/%s' % id
			
			body = 'name=%s'	% name
			body += '&program=%s'	% program
		
			response, content = connection.request(url, method='POST', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, body=body)
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
			
		return None

	def deleteApplication(self, id=None):
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application/%s' % id
			
			response, content = connection.request(url, method='DELETE', headers={}, body='')
			
			if response.status == 200:
				data = json.loads(content)
				return self.checkData(data)
		except:
			pass
			
		return None

	def detailApplication(self, id=None):
		try:
			response = urllib2.urlopen(self.host + '/api/v1/application/%s' % id)
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return None

	def listApplications(self):
		#so simple
		try:
			response = urllib2.urlopen(self.host + '/api/v1/application')
			
			if response.getcode() == 200:
				raw = response.read()
				
				data = json.loads(raw)
				
				return self.checkData(data)
		except:
			pass
			
		return None
