from _db import APIDB

db = None

def connect():
  global db
  db = APIDB()
  
  if db == None:
    return False
  
  return True
