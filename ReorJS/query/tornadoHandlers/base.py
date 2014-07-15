import tornado.web
import simplejson as json

class BaseHandler(tornado.web.RequestHandler):
  def get(self):
    print "Tornado get needs to be overridden"
  
  def post(self):
    print "Tornado post needs to be overridden"
  
  def delete(self):
    print "Tornado delete needs to be overridden"
                        
  def put(self):
    print "Tornado put needs to be overridden"
    
  def options(self):
    print "Tornado options needs to be overridden"
