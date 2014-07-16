from sqlalchemy import *
from sqlalchemy.orm import *

from base import Base

class Application(Base):
  __tablename__ = 'application'
  
  uid = Column(Integer, primary_key=True)
  name = Column(String)
  program = Column(String)
  
  def __init__(self, name=None, program=None):
    self.name = name
    self.program = program
  
  def __repr__(self):
    return "<Application('%s')>" % self.uid
  
  def to_serializable_object(self):
    return {
      'uid' : self.uid,
      'name' : self.name,
      'program' : self.program,
    }
