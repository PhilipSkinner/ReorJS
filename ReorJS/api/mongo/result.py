from mongoengine import *
from task import *

class TaskResult(Document):
  task = IntField()
  data = StringField()
  timeTaken = IntField()
  received = DateTimeField()

  meta = {
    'ordering' : ['task'],
    'indexes' : ['task', ('id', 'received',)],
  }
  
  def __repr__(self):
    return '%s(%s)' % (self.task, self.id)
  
  def __unicode__(self):
    return self.__repr__()
  
  def __str__(self):
    return self.__repr__()
  
