from base import *

class APIApplicationHandler(BaseHandler):
  def get(self, id=None):
    self.application.ApplicationHandler.get()
