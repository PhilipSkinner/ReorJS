from base import *

class APITaskHandler(BaseHandler):
  def get(self, id=None):
    self.application.TaskHandler.setParent(self)
    
    if id == '':
      id = None
  
    self.application.TaskHandler.get(id=id)
  
  def post(self, id=None):
    self.application.TaskHandler.setParent(self)
    
    if id == '':
      id = None
      
    self.application.TaskHandler.post(id=id)
