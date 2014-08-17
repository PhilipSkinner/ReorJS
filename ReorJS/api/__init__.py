from _db import APIDB

db = None

def connect():
  db = APIDB()
  
  if db == None:
    return False
  
  return True
