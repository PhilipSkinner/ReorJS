from _db import APIDB

db = None

def connect():
  global db
  db = APIDB()
  
  return db.ready
