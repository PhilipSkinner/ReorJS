from base import BaseQueryService
import settings
import handlers as _handlers

_app = None

class QueryTornado(BaseQueryService):
	def __init__(self):
		print "Setting up Tornado"
		import tornado.httpserver
		import tornadoHandlers
		
		urls = [
			(r'/api/v1/dataset/(.*)/data', tornadoHandlers.APIDataSetHandler),
			(r'/api/v1/dataset/?(.*)', tornadoHandlers.APIDataSetHandler),
			(r'/api/v1/task/?(.*)', tornadoHandlers.APITaskHandler),
			(r'/api/v1/application/?(.*)', tornadoHandlers.APIApplicationHandler),
		]
		
		self.application = TornadoApp(urls)
		self.server = tornado.httpserver
		self.application.listen(settings.PORT)

	def start(self):
		print "Running tornado"	
		import tornado.ioloop		
		tornado.ioloop.IOLoop.instance().start()

def TornadoApp(handlers=None):
	global _app
	if not _app:
		import tornado.web

                class TornadoAppObject(tornado.web.Application):
                        def __init__(self, handlers):
                                super(TornadoAppObject, self).__init__(handlers)                
				
                		self.DataSetDataHandler = _handlers.APIDataSetDataHandler()
                                self.DataSetHandler = _handlers.APIDataSetHandler()
                                self.TaskHandler = _handlers.APITaskHandler()
                                self.ApplicationHandler = _handlers.APIApplicationHandler()                

		_app = TornadoAppObject(handlers)
	
	return _app