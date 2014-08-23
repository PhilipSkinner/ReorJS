from base import BaseQueryService
import settings
import handlers
import re

class QueryFAPWS(BaseQueryService):
	def __init__(self):
		print "Setting up FAPWS"

		import fapws._evwsgi as evwsgi		
		self.server = evwsgi
		
		#create our handlers
		self.DataSetDataHandler = handlers.APIDataSetDataHandler(self)
		self.DataSetHandler = handlers.APIDataSetHandler(self)
		self.TaskHandler = handlers.APITaskHandler(self)
		self.ApplicationHandler = handlers.APIApplicationHandler(self)				
	
	def start(self):
		print "Running FAPWS"
		from fapws import base
		
		self.server.start(settings.IP, settings.PORT)
		self.server.set_base_module(base)
		
		self.server.wsgi_cb(('/api/v1/dataset/(.*)/data', self.data_set_data_handler)),
		self.server.wsgi_cb(('/api/v1/dataset/', self.data_set_handler)),
		self.server.wsgi_cb(('/api/v1/dataset', self.data_set_handler)),
		self.server.wsgi_cb(('/api/v1/task/', self.task_handler)),
		self.server.wsgi_cb(('/api/v1/task', self.task_handler)),
		self.server.wsgi_cb(('/api/v1/application/(.*)', self.application_handler)),
		self.server.wsgi_cb(('/api/v1/application', self.application_handler)),
		
		self.server.run()
		
	def data_set_data_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.DataSetDataHandler.setParent(resp)
		
		ret = self.DataSetDataHandler.get()
		
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
		
		self.DataSetHandler.get(id=id)

		resp.headers()
		return [resp.response]

	def task_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.TaskHandler.setParent(resp)
		
		ret = self.TaskHandler.get(id=id)

		resp.headers()
		return [resp.response]

	def application_handler(self, environ, start_response):
		id = None
		if 'PATH_INFO' in environ and environ['PATH_INFO'] != None:
			id = environ['PATH_INFO'].replace('/', '')
			
		#handlers.APIDataSetHandler
		resp = FAPWSResponse(environ, start_response)
		self.ApplicationHandler.setParent(resp)
		
		ret = self.ApplicationHandler.get(id=id)
  
		resp.headers()
		return [resp.response]

class FAPWSResponse():
	def __init__(self, environ, start_response):
		self.response = ''
		self._headers = []
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
