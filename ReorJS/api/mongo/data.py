from mongoengine import *
from task import *

import datetime
import calendar

class Dataset(Document):
  name = StringField()
  created = DateTimeField(default=datetime.datetime.utcnow)

  def to_object(self):
    return {
      'id': str(self.id),
      'name': self.name,
      'created': str(self.created),
    }

class DatasetData(Document):
  customid = StringField()
  data = StringField()
  dataset = IntField()

  meta = {
    'ordering' : ['dataset'],
    'indexes' : ['dataset'],
  }

  def __repr__(self):
    return '%s(%s)' % (self.dataset, self.customid)

  def __unicode__(self):
    return self.__repr__()

class TaskDataset(Document):
  task = ReferenceField(Task)
  dataset = ReferenceField(Dataset)

  meta = {
    'ordering' : ['task'],
    'indexes' : ['task'], 
  }

class TaskData(Document):
  task = ReferenceField(Task)
  customid = StringField()
  data = StringField() #store just as a string so no parsing done locally
  result = StringField()
  time = FloatField()
  completed = BooleanField(default=False)
  completedOn = DateTimeField()
  stacked = BooleanField(default=False)
  stacker = ReferenceField('Stacker')
  sent = BooleanField(default=False)
  sentOn = DateTimeField()

  meta = {
    'ordering' : ['task'],
    'indexes' : ['task', 'completed', 'stacked',
      ('task', 'completed'),
      ('task', 'completed', 'stacked',),
      ('sent', 'completed', 'sentOn')],
  }

  def __repr__(self):
    return '%s(%s)' % (self.task, self.id)

  def __unicode__(self):
    return self.__repr__()

  def __str__(self):
    return self.__repr__()

  def to_result_object(self):
    return {
      'customid': self.customid,
      'data': self.data,
      'result': self.result,
      'time': self.time,
      'completedOn': calendar.timegm(self.completedOn.timetuple())
    }
