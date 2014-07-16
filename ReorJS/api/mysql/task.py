from sqlalchemy import *
from sqlalchemy.orm import *

from base import Base

class Task(Base):
  __tablename__ = 'task'
  
  uid = Column(Integer, primary_key=True)
  task = Column(Integer)
  owner = Column(Integer)
  dataset_id = Column('dataset', Integer, ForeignKey('dataset.uid'))
  result_id = Column('result', Integer, ForeignKey('dataset.uid'))
  application_id = Column('application', Integer, ForeignKey('application.uid'))
  program = Column(String)
  
  dataset = relationship('Dataset', primaryjoin='Task.dataset_id == Dataset.uid', backref=backref('task_input', order_by=uid))
  result = relationship('Dataset', primaryjoin='Task.result_id == Dataset.uid', backref=backref('task_output', order_by=uid))
  application = relationship('Application', primaryjoin='Task.application_id == Application.uid', backref=backref('tasks', order_by=uid))
  
  def __init__(self, task=None, owner=None, datase_id=None, result_id=None, application_id=None, program=None):
    self.task = task
    self.owner = owner
    self.datasetId = dataset_id
    self.resultId = result_id
    self.applicationId = application_id
    self.program = program
    
  def __repr__(self):
    return "<Task('%s')>" % self.uid
  
  def to_serializable_object(self):
    return {
      'uid' : self.uid,
      'task' : self.task,
      'owner' : self.owner,
      'dataset' : self.dataset_id,
      'result' : self.result_id,
      'application' : self.application_id,
      'program' : self.program,
    }
