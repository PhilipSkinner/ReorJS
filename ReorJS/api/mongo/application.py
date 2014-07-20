from mongoengine import *

class Application(Document):
  name = StringField()
  program = StringField()

  def __init__(self, name=None, program=None):
    self.name = name
    self.program = program

  def __repr__(self):
    return "<Application('%s')>" str(self.id)

  def __unicode__(self):
    return self.__repr__()

  def to_serializable_object(self):
    return {
      'id': str(self.id),
      'name': self.name,
      'program' : self.program,
    }
