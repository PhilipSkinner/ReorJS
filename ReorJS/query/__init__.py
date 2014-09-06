import settings
import logger
from queryfapws import QueryFAPWS
from querytornado import QueryTornado
from querybasehttpserver import QueryBaseHTTPServer

import output
import input

class QueryService():
  def __init__(self):
    self.tornado = None
    self.fapws = None
    self.base = None
    
    self.output = output.OutputService()
    self.input = input.InputService()
    
    if settings.HTTP_SERVICE == 'tornado':
      logger.LOG.log("Setting up Tornado")
      
      self.tornado = QueryTornado(output=self.output, input=self.input)
    elif settings.HTTP_SERVICE == 'fapws':
      logger.LOG.log("Setting up fapws")
      
      self.fapws = QueryFAPWS(output=self.output, input=self.input)      
    elif settings.HTTP_SERVICE == 'base':
      logger.LOG.log("Setting up BaseHTTPServer")
      
      self.base = QueryBaseHTTPServer(output=self.output, input=self.input)
  
  def run(self):
    if self.tornado != None:
      logger.LOG.log("Running tornado service")
      
      self.tornado.start()
    elif self.fapws != None:
      logger.LOG.log("Running fapws service")

      self.fapws.start()      
    elif self.base != None:
      logger.LOG.log("Running BaseHTTPServer service")
      
      self.base.start()
