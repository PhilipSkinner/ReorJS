import settings
from queryfapws import QueryFAPWS
from querytornado import QueryTornado
from querybasehttpserver import QueryBaseHTTPServer

import output

class QueryService():
  def __init__(self):
    self.tornado = None
    self.fapws = None
    self.base = None
    
    self.output = output.OutputService()
    
    if settings.HTTP_SERVICE == 'tornado':
      print "Setting up Tornado"
      
      self.tornado = QueryTornado(output=self.output)
    elif settings.HTTP_SERVICE == 'fapws':
      print "Setting up fapws"
      
      self.fapws = QueryFAPWS(output=self.output)      
    elif settings.HTTP_SERVICE == 'base':
      print "Setting up BaseHTTPServer"
      
      self.base = QueryBaseHTTPServer(output=self.output)
  
  def run(self):
    if self.tornado != None:
      print "Running tornado service"
      
      self.tornado.start()
    elif self.fapws != None:
      print "Running fapws service"

      self.fapws.start()      
    elif self.base != None:
      print "Running BaseHTTPServer service"
      
      self.base.start()
