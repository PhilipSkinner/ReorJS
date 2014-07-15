from mongoengine import *

class Stacker(Document):
  ip = StringField()
  port = IntField()
  status = BooleanField(default=False)  
  
  meta = {
    'ordering' : ['status'],
    'indexes' : ['status', 'ip', 'port'],
  }
  
  def delete_tasks(self):
    import data
    data.TaskData.objects(stacker=self, stacked=True, completed=False).update(
      set__stacked=False, set__stacker=None)

  def __repr__(self):
    return '%s(%s)' % (self.ip, self.port)
  
  def __unicode__(self):
    return self.__repr__()
  
  def __str__(self):
    return self.__repr__()
