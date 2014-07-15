from mongoengine import *

class Task(Document):
  task = IntField()
  owner = IntField()
  dataset = IntField()
  result = IntField()
  application = IntField()
  program = StringField()
  ppd = FloatField(min_value=0)

  meta = {
    'ordering' : ['task'],
    'indexes' : ['task', 'owner', 'ppd'],
  }

  def to_object(self):
    return {
      'id': str(self.id),
    }

  def __repr__(self):
    return '%s(%s)' % (self.owner, self.task)

  def __unicode__(self):
    return self.__repr__()

  def __str__(self):
    return self.__repr__()
