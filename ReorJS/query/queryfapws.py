from base import BaseQueryService
import settings
import handlers

class QueryFAPWS(BaseQueryService):
	def __init__(self):
		print "Setting up FAPWS"

		import fapws._evwsgi as evwsgi		
		self.server = evwsgi
		
		#create our handlers
		self.DataSetDataHandler = handlers.APIDataSetDataHandler()
		self.DataSetHandler = handlers.APIDataSetHandler()
		self.TaskHandler = handlers.APITaskHandler()
		self.APIApplicationHandler = handlers.APIApplicationHandler()
	
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
		self.server.wsgi_cb(('/api/v1/application/', self.application_handler)),
		self.server.wsgi_cb(('/api/v1/application', self.application_handler)),
		
		self.server.run()

	def data_set_data_handler(self, environ, start_response):
		#handlers.APIDataSetHandler
		ret = self.DataSetDataHandler.get()
		
		if ret == None:
			return ['']

	def data_set_handler(self, environ, start_response):
		#handlers.APIDataSetHandler
		ret = self.DataSetHandler.get()

		if ret == None:
			return ['']

	def task_handler(self, environ, start_response):
		#handlers.APIDataSetHandler
		ret = self.TaskHandler.get()

		if ret == None:
			return ['']

	def application_handler(self, environ, start_response):
		#handlers.APIDataSetHandler
		ret = self.ApplicationHandler.get()
  
		if ret == None:
			return ['']
