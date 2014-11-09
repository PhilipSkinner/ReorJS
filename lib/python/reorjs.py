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

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import httplib2
import simplejson as json

class ReorJS():
	"""
	Provides simple programmatic access to the ReorJS server for API calls.

	<code>
	import reorjs
	api = reorjs.ReorJS()
	api.setHost('http://localhost:9999')
	api.setKey('temporary')
	print api.listApplications()
	</code>
	"""

	def __init__(self):
		"""
		Construct a new ReorJS object with default values
		"""
		self.host = 'http://localhost:9999' #default
		self.key = ''

	def setHost(self, host):
		"""
		Sets the ReorJSd host to be used for requests.

		Needs to be in the format:

		http://[host]:[port]
		"""
		self.host = host

	def setKey(self, key):
		"""
		Sets the access key to be used for authentication.
		"""
		self.key = key

	def connectionTest(self):
		"""
		Attempts to test the connection to the ReorJSd service
		"""
		#simply connect to the server
		try:
			response = urllib.request.urlopen(self.host + '/output/v1/ping?key=%s' % self.key)

			if response.getcode() == 200:
				return True
		except:
			pass

		return False

	def detailTask(self, id=None):
		"""
		Returns details for a particular task in the system.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/task/%s?key=%s' % (id, self.key))

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return {}

	def createTask(self, application=None, dataset=None, result=None):
		"""
		Creates a task in the system.
		"""
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/task'
			body = urllib.parse.urlencode({
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
		"""
		Lists all of the tasks currently in the system.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/task?key=%s' % (self.key))

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return []

	def createDataset(self, name=None, source_type=None, source_hostname=None, source_port=None, source_name=None, source_table=None, source_username=None, source_password=None):
		"""
		Creates a new dataset (or source) in the system.
		"""
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/dataset'

			body = urllib.parse.urlencode({
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
		"""
		Modifies an existing dataset.
		"""
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/dataset/%s' % id

			body = urllib.parse.urlencode({
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
		"""
		Deletes a dataset.
		"""
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
		"""
		Returns details for a dataset.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/dataset/%s?key=%s' % (id, self.key))

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return {}

	def listDatasets(self):
		"""
		Returns a list of the datasets in the system.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/dataset?key=%s' % (self.key))

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return []

	def createApplication(self, name=None, program=None):
		"""
		Creates a new application.
		"""
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application'

			body = urllib.parse.urlencode({
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
		"""
		Modifies an application.
		"""
		try:
			connection = httplib2.Http()
			url = self.host + '/api/v1/application/%s' % id

			body = urllib.parse.urlencode({
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
		"""
		Deletes an application.
		"""
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
		"""
		Returns the details for an application.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/application/%s?key=%s' % (id, self.key))

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return {}

	def listApplications(self):
		"""
		Lists all of the applications
		"""
		try:
			response = urllib.request.urlopen(self.host + '/api/v1/application?key=%s' % self.key)

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return []

	def ping(self):
		"""
		Pings the output service.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/output/v1/ping?key=%s' % self.key)

			if response.getcode() == 200:
				raw = response.read()

				data = { 'error' : 'Could not reach output service', 'code' : '9002' }

				if raw == 'PONG':
					data = { 'status' : { 'message' : 'PONG received!' }, 'code' : '200' }

				return data
		except:
			pass

		return { 'error' : 'Could not reach output service', 'code' : '9002' }

	def status(self):
		"""
		Fetches the current status of the stacker system.
		"""
		try:
			response = urllib.request.urlopen(self.host + '/output/v1/status?key=%s' % self.key)

			if response.getcode() == 200:
				raw = response.read()

				data = json.loads(raw)

				return self.checkData(data)
		except:
			pass

		return {}

	def _checkData(self, data):
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
