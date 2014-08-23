import urllib2
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
				if str(data['meta']['code']) == '200' and 'data' in data:
					return data['data']
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
