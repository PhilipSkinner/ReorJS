"""
        query/querytornado.py
        ReorJSd Tornado Query Service
          
        --
        Uses Tornado to create and handle all HTTP requests to the ReorJSd services.       
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
import logger
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
		logger.LOG.log("Running tornado")
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
