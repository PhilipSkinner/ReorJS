"""
	query/queryfapws.py
	ReorJSd FAPWS Query Service
        
        --
	Uses FAPWS to create and handle all HTTP requests to the ReorJSd services.
        --
        
        Author(s)       - Philip Skinner (philip@crowdca.lc)
        Last modified   - 2014-09-28
        
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

from base import BaseQueryService
import settings
import handlers
import re

class QueryFAPWS(BaseQueryService):
	def __init__(self, output=None, input=None):
		logger.LOG.log("Setting up FAPWS")

		import fapws._evwsgi as evwsgi		
		self.server = evwsgi
		
		#create our handlers
		self.DataSetDataHandler = handlers.APIDataSetDataHandler(self)
		self.DataSetHandler = handlers.APIDataSetHandler(self)
		self.TaskHandler = handlers.APITaskHandler(self)
		self.ApplicationHandler = handlers.APIApplicationHandler(self)
		
		if output != None:
			self.output = output
		
		if input != None:
			self.input = input
	
	def start(self):
		logger.LOG.log("Running FAPWS")
		from fapws import base
		
		self.server.start(settings.IP, settings.PORT)
		self.server.set_base_module(base)
		
		self.server.wsgi_cb(('/api/v1/dataset/(.*)/data', self.data_set_data_handler))
		self.server.wsgi_cb(('/api/v1/dataset/', self.data_set_handler))
		self.server.wsgi_cb(('/api/v1/dataset', self.data_set_handler))
		self.server.wsgi_cb(('/api/v1/task/', self.task_handler))
		self.server.wsgi_cb(('/api/v1/task', self.task_handler))
		self.server.wsgi_cb(('/api/v1/application/(.*)', self.application_handler))
		self.server.wsgi_cb(('/api/v1/application', self.application_handler))
		
		if self.output != None:
			self.server.wsgi_cb(('/output/v1/task', self.get_task_handler))
			self.server.wsgi_cb(('/output/v1/ping', self.ping_handler))
			self.server.wsgi_cb(('/output/v1/status', self.status_handler))
		
		if self.input != None:
			self.server.wsgi_cb(('/input/v1/result', self.receive_result_handler))
		
		self.server.run()
		
	##
	# Input handlers
	##
		
	def receive_result_handler(self, environ, start_response):
		resp = FAPWSResponse(environ, start_response)
		self.input.ReceiveResultHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			ret = self.input.ReceiveResultHandler.get()
		elif method == 'POST':
			ret = self.input.ReceiveResultHandler.post()
		elif method == 'DELETE':
			ret = self.input.ReceiveResultHandler.delete()
		elif method == 'PUT':
			ret = self.input.ReceiveResultHandler.put()
		
		resp.headers()
		return [resp.response]
		
	##
	# Output handlers
	##
	
	def get_task_handler(self, environ, start_response):
		resp = FAPWSResponse(environ, start_response)
		self.output.GetTaskHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			ret = self.output.GetTaskHandler.get()		
		elif method == 'POST':
			ret = self.output.GetTaskHandler.post()		
		elif method == 'DELETE':
			ret = self.output.GetTaskHandler.delete()		
		elif method == 'PUT':
			ret = self.output.GetTaskHandler.put()
		
		resp.headers()
		return [resp.response]
	
	def ping_handler(self, environ, start_response):
		resp = FAPWSResponse(environ, start_response)
		self.output.PingHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':		
			ret = self.output.PingHandler.get()		
		elif method == 'POST':
			ret = self.output.PingHandler.post()				
		elif method == 'DELETE':
			ret = self.output.PingHandler.delete()		
		elif method == 'PUT':
			ret = self.output.PingHandler.put()		
		
		resp.headers()
		return [resp.response]
	
	def status_handler(self, environ, start_response):
		resp = FAPWSResponse(environ, start_response)
		self.output.StatusHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':		
			ret = self.output.StatusHandler.get()
		elif method == 'POST':
			ret = self.output.StatusHandler.post()
		elif method == 'DELETE':
			ret = self.output.StatusHandler.delete()
		elif method == 'PUT':
			ret = self.output.StatusHandler.put()
		
		resp.headers()
		return [resp.response]
	
	##
	# End - Output handlers
	##
		
	def data_set_data_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.DataSetDataHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			ret = self.DataSetDataHandler.get()		
		elif method == 'POST':
			ret = self.DataSetDataHandler.post()		
		elif method == 'DELETE':
			ret = self.DataSetDataHandler.delete()		
		elif method == 'PUT':
			ret = self.DataSetDataHandler.put()
		
		resp.headers()
		return [resp.response]

	def data_set_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO']
			
			if re.match("\d+\/data", id):
				return self.data_set_data_handler(environ, start_response)
			
			id = id.replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.DataSetHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			self.DataSetHandler.get(id=id)		
		elif method == 'POST':
			self.DataSetHandler.post(id=id)		
		elif method == 'DELETE':
			self.DataSetHandler.delete(id=id)		
		elif method == 'PUT':
			self.DataSetHandler.put(id=id)

		resp.headers()
		return [resp.response]

	def task_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.TaskHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			ret = self.TaskHandler.get(id=id)				
		elif method == 'POST':
			ret = self.TaskHandler.post(id=id)				
		elif method == 'DELETE':
			ret = self.TaskHandler.delete(id=id)		
		elif method == 'PUT':
			ret = self.TaskHandler.put(id=id)

		resp.headers()
		return [resp.response]

	def application_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
		
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.ApplicationHandler.setParent(resp)
		
		method = self.determine_method(environ)
		
		if method == 'GET':
			ret = self.ApplicationHandler.get(id=id)		
		elif method == 'POST':
			ret = self.ApplicationHandler.post(id=id)		
		elif method == 'DELETE':
			ret = self.ApplicationHandler.delete(id=id)		
		elif method == 'PUT':
			ret = self.ApplicationHandler.put(id=id)
  
		resp.headers()
		return [resp.response]
	
	def determine_method(self, environ):
		if 'REQUEST_METHOD' in environ:
			return environ['REQUEST_METHOD']
		else:
			return 'GET'

class FAPWSResponse():
	def __init__(self, environ, start_response):
		self.response = ''
		self._headers = [		
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Headers', 'X-Request, X-Requested-With'),
                        ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT'),
                        ('Access-Control-Max-Age', '1728000'),
		]
		self.environ = environ
		self.start_response = start_response		

	def headers(self):
		self.start_response('200 OK', self._headers)
			
	def get_argument(self, name, default):
		params = self.environ['fapws.params']
		
		return params.get(name, [default])[0]
		
	def set_header(self, name, value):
		self._headers.append((name, value))
		
	def write(self, value):
		self.response = '%s%s' % (self.response, value)
