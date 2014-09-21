import logging
import settings

class Logger():
  def __init__(self, logfile, level):
    logging.basicConfig(filename=logfile,level=level,format='%(asctime)-15s - [%(processName)s,%(process)d] - %(message)s')
    logging.info("Started logging")

  def critical(self, value):
    logging.error(value)

  def error(self, value):
    logging.error(value)

  def log(self, value):
    logging.warning(value)

  def info(self, value):
    logging.info(value)
  
  def debug(self, value):
    logging.debug(value)

LOG = None

def initLogger():
  global LOG
  level = logging.WARNING
  
  if settings.VERBOSE or settings.VERBOSE == "True":
    level = logging.INFO
  
  if settings.DEBUG or settings.DEBUG == "True":
    level = logging.DEBUG
  
  LOG = Logger('%s/reorjsd.log' % settings.LOG_LOCATION, level)
