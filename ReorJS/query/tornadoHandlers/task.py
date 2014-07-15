from base import *

class APITaskHandler(BaseHandler):
  def get(self, id=None):
    self.application.TaskHandler.get()
