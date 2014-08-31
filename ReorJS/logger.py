import logging
import settings
import os

class LogFile(logging.getLoggerClass()):
  def __init__(self, logfile, level):
    self.basicConfig(filename=logfile,level=level)      

class Logger():
  def __init__(self):
    #ensure our log file directory exists
    parts = settings.LOG_LOCATION.split('/')
    path = ''
    for p in parts:
      if p != '':
        path += '/%s' % p
        
        if not os.path.isdir(path):
          os.makedirs(path)
  
    self.system 	= LogFile('%s/reorjs.system.log' % settings.LOG_LOCATION, logging.INFO)
    self.api	 	= LogFile('%s/reorjs.api.log' % settings.LOG_LOCATION, logging.INFO)
    self.stacker 	= LogFile('%s/reorjs.stacker.log' % settings.LOG_LOCATION, logging.INFO)

LOG = None
