from base import BaseQueryService
import settings
import handlers as _handlers

_app = None

class QueryTornado(BaseQueryService):
	def __init__(self, output=None, input=None):
		import tornado.httpserver
		import tornadoHandlers
		
		urls = [
			(r'/api/v1/dataset/(.*)/data', tornadoHandlers.APIDataSetHandler),
			(r'/api/v1/dataset', tornadoHandlers.APIDataSetHandler),
			(r'/api/v1/dataset/?(.*)', tornadoHandlers.APIDataSetHandler),
			(r'/api/v1/task', tornadoHandlers.APITaskHandler),
			(r'/api/v1/task/?(.*)', tornadoHandlers.APITaskHandler),
			(r'/api/v1/application', tornadoHandlers.APIApplicationHandler),
			(r'/api/v1/application/?(.*)', tornadoHandlers.APIApplicationHandler),
		]
		
		if output != None:
		        self.output = output
        	        urls.append((r'/output/v1/task', tornadoHandlers.GetTask))
	                urls.append((r'/output/v1/ping', tornadoHandlers.Ping))
	                urls.append((r'/output/v1/status', tornadoHandlers.Status))
                
                if input != None:
                        self.input = input
                        urls.append((r'/input/v1/result', tornadoHandlers.ReceiveResult))        
		
		self.application = TornadoApp(urls, output, input)
		self.server = tornado.httpserver
		self.application.listen(settings.PORT)

	def start(self):
		print "Running tornado"	
		import tornado.ioloop		
		tornado.ioloop.IOLoop.instance().start()

def TornadoApp(handlers=None, output=None, input=None):
	global _app
	if not _app:
		import tornado.web

                class TornadoAppObject(tornado.web.Application):
                        def __init__(self, handlers, output, input):
                                super(TornadoAppObject, self).__init__(handlers)                
				
                		self.DataSetDataHandler = _handlers.APIDataSetDataHandler(self)
                                self.DataSetHandler = _handlers.APIDataSetHandler(self)
                                self.TaskHandler = _handlers.APITaskHandler(self)
                                self.ApplicationHandler = _handlers.APIApplicationHandler(self)                                                                
                                
                                self.output = output
                                self.input = input
                                
		_app = TornadoAppObject(handlers, output, input)
	
	return _app
