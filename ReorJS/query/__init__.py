import settings
from queryfapws import QueryFAPWS
from querytornado import QueryTornado
from querybasehttpserver import QueryBaseHTTPServer

class QueryService():
  def __init__(self):
    self.tornado = None
    self.fapws = None
    self.base = None
    
    print settings.HTTP_SERVICE
    
    if settings.HTTP_SERVICE == 'tornado':
      print "Setting up Tornado"
      
      self.tornado = QueryTornado()
    elif settings.HTTP_SERVICE == 'fapws':
      print "Setting up fapws"
      
      self.fapws = QueryFAPWS()      
    elif settings.HTTP_SERVICE == 'base':
      print "Setting up BaseHTTPServer"
      
      self.base = QueryBaseHTTPServer()
  
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
