import tornado.web
import simplejson as json
import logger

class BaseHandler(tornado.web.RequestHandler):
  def prepare(self):
    self.set_header('Access-Control-Allow-Origin', '*')
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
    self.set_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
    self.set_header('Access-Control-Max-Age', '1728000')

  def get(self):
    logger.LOG.log("Tornado get needs to be overridden")
  
  def post(self):
    logger.LOG.log("Tornado post needs to be overridden")
  
  def delete(self):
    logger.LOG.log("Tornado delete needs to be overridden")
                        
  def put(self):
    logger.LOG.log("Tornado put needs to be overridden")
    
  def options(self):
    logger.LOG.log("Tornado options needs to be overridden")
