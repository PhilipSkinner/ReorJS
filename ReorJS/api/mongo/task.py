from mongoengine import *

from data import *
from application import *

class Task(Document):
  task = IntField()
  owner = IntField()
  dataset_id = StringField()
  result_id = StringField()
  application_id = StringField()
  program = Column(String)
  
  dataset = ReferenceField('Dataset')
  result = ReferenceField('Dataset')
  application = ReferenceField('Application')

  meta = {
    'ordering' : ['task'],
    'indexes' : ['task', 'owner'],
  }
  
  def __init__(self, task=None, owner=None, dataset_id=None, result_id=None, application_id=None, program=None):
    self.task = task
    self.owner = owner
    self.dataset_id = dataset_id
    self.result_id = result_id
    self.application_id = application_id
    self.program = program
    
    #now for reference fields
    self.dataset = Dataset.objects(id = self.dataset_id).first()
    self.result = Dataset.objects(id = self.result_id).first()
    self.application = Application.objects(id = self.application_id).first()

  def __repr__(self):
    return "<Task('%s')>" % str(self.id)

  def __unicode__(self):
    return self.__repr__()

  def to_serializable_object(self):
    return {
      'id': str(self.id),
      'task' : self.task,
      'owner' : self.owner,
      'dataset' self.dataset_id,
      'result' : self.result_id,
      'application' : self.application_id,
      'program' : self.program,
    }

