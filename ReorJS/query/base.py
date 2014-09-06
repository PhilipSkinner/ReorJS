class BaseQueryService():
  def __init__(self, output=None):
    logger.LOG.log("Initialization needs to be overridden")
    
  def start(self):
    logger.LOG.log("Startup methods needs to be overridden")
