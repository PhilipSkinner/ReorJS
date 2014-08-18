from base import *

class APIApplicationHandler(BaseHandler):
  def get(self, id=None):
    self.application.ApplicationHandler.setParent(self)
  
    if id == '':
      id = None
      
    self.application.ApplicationHandler.get(id=id)

  def post(self, id=None):
    self.application.ApplicationHandler.setParent(self)
  
    if id == '':
      id = None
      
    self.application.ApplicationHandler.post(id=id)
  
  def delete(self, id=None):
    self.application.ApplicationHandler.setParent(self)
    
    if id == '':
      id = None
    
    self.application.ApplicationHandler.delete(id=id)
