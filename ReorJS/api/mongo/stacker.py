from mongoengine import *

class Stacker(Document):
  ip = StringField()
  port = IntField()
  status = BooleanField()

  def __init__(self, ip=None, port=None, status=None):
    self.ip = ip
    self.port = port
    self.status = status

  def __repr__(self):
    return "<Stacker('%s')>" str(self.id)

  def __unicode__(self):
    return self.__repr__()

  def to_serializable_object(self):
    return {
      'id': str(self.id),
      'ip' : self.ip,
      'port' : self.port,
      'status' : self.status,
    }
