from sqlalchemy import *
from sqlalchemy.orm import *

from base import Base

class Stacker(Base):
  __tablename__ = 'stacker'
  
  uid = Column(Integer, primary_key=True)
  ip = Column(String)
  port = Column(Integer)
  status = Column(Boolean)
  
  def __init__(self, ip=None, port=None, status=False):
    self.ip = ip
    self.port = port
    self.status = status
  
  def __repr__(self):
    return "<Stacker('%s')>" % self.uid
  
  def to_serializable_object(self):
    return {
      'uid' : self.uid,
      'ip' : self.ip,
      'port' : self.port,
      'status' : self.status,
    }
