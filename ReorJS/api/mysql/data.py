from sqlalchemy import *
from sqlalchemy.orm import *

from base import Base

import datetime

class Dataset(Base):
  __tablename__ = 'dataset'

  uid = Column(Integer, primary_key=True)
  name = Column(String)
  source_type = Column(String)
  source_name = Column(String)
  source_hostname = Column(String)
  source_port = Column(String)
  source_username = Column(String)
  source_password = Column(String)
  created = Column(DateTime)
  
  def __init__(self, name=None, source_type=None, source_name=None, source_hostname=None, source_port=None, source_username=None, source_password=None):
    self.name = name
    self.source_type = source_type
    self.source_name = source_name
    self.source_hostname = source_hostname
    self.source_port = source_port
    self.source_username = source_username
    self.source_password = source_password
    self.created = datetime.datetime.now()
  
  def __repr__(self):
    return "<Dataset('%s')>" % self.uid
  
  def to_serializable_object(self):
    return {
      'uid' : self.uid,
      'name' : self.name,
      'source_type' : self.source_type,
      'source_name' : self.source_name,
      'source_hostname' : self.source_hostname,
      'source_port' : self.source_port,
      'source_username' : self.source_username,
      'source_password' : self.source_password,
      'created' : str(self.created),
    }

def DatasetData(Base):
  __tablename__ = 'dataset_data'
  
  uid = Column(Integer, primary_key=True)
  dataset_id = Column('dataset', Integer, ForeignKey('dataset.uid'))
  custom_id = Column(String)
  data = Column(String)
  
  dataset = relationship('Dataset', primaryjoin='DatasetData.dataset_id == Dataset.uid', backref=backref('data', order_by=uid))
  
  def __init__(self, dataset_id=None, custom_id=None, data=None):
    self.dataset_id = dataset_id
    self.custom_id = custom_id
    self.data = data
  
  def __repr__(self):
    return "<DatasetData('%s')>" % self.uid
  
  def to_serializable_object(self):
    return {
      'uid' : self.uid,
      'dataset' : self.dataset_id,
      'custom_id' : self.custom_id,
      'data' : self.data,
    }
  
