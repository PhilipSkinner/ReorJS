from sqlalchemy import *
from sqlalchemy.orm import *

from base import Base

class Task(Base):
  __tablename__ = 'task'
  
  id = Column(Integer, primary_key=True)
  task = Column(Integer)
  owner = Column(Integer)
  dataset_id = Column('dataset', Integer, ForeignKey('dataset.id'))
  result_id = Column('result', Integer, ForeignKey('dataset.id'))
  application_id = Column('application', Integer, ForeignKey('application.id'))
  program = Column(String)
  
  dataset = relationship('Dataset', primaryjoin='Task.dataset_id == Dataset.id', backref=backref('task_input', order_by=id))
  result = relationship('Dataset', primaryjoin='Task.result_id == Dataset.id', backref=backref('task_output', order_by=id))
  application = relationship('Application', primaryjoin='Task.application_id == Application.id', backref=backref('tasks', order_by=id))
  
  def __init__(self, task=None, owner=None, dataset_id=None, result_id=None, application_id=None, program=None):
    self.task = task
    self.owner = owner
    self.dataset_id = dataset_id
    self.result_id = result_id
    self.application_id = application_id
    self.program = program
    
  def __repr__(self):
    return "<Task('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' : self.id,
      'task' : self.task,
      'owner' : self.owner,
      'dataset' : self.dataset_id,
      'result' : self.result_id,
      'application' : self.application_id,
      'program' : self.program,
    }
