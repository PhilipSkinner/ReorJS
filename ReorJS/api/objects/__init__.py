from application import *
from task import *
from data import *
from stacker import *

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.sql import *

_connection = None
_rawConnection = None
_session = None

def connection(username=None, password=None, host=None, port=None, name=None):
  global _connection
  
  if _connection == None:
    _connection = create_engine("mysql://%s:%s@%s:%s/%s" % (username, password, host, port, name),
                                  encoding="utf8", convert_unicode=True, pool_recycle=600, poolclass=SingletonThreadPool, echo=False)
  
  c = _connection.connect()
  
  return _connection

def Session(username=None, password=None, host=None, port=None, name=None):
  global _session
  
  if _session == None:
    _session = scoped_session(sessionmaker(bind=connection(username=username, password=password, host=host, port=port, name=name)))
  
  return _session
