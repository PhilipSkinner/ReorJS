import logging
import settings

class Logger():
  def __init__(self, logfile, level):
    logging.basicConfig(filename=logfile,level=level)
    logging.info("Started logging")

  def log(self, value):
    logging.info(value)

LOG = None

def initLogger():
  global LOG
  LOG = Logger('%s/reorjsd.log' % settings.LOG_LOCATION, logging.INFO)
