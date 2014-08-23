from base import *

class GetTask(BaseHandler):
  def get(self):
    self.application.output.GetTaskHandler.setParent(self)
    
    self.application.output.GetTaskHandler.get()

class Ping(BaseHandler):
  def get(self):
    self.application.output.PingHandler.setParent(self)
    
    self.application.output.PingHandler.get()
    
class Status(BaseHandler):
  def get(self):
    self.application.output.StatusHandler.setParent(self)
    
    self.application.output.StatusHandler.get()
