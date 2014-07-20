from mongoengine import *
from task import *

import datetime
import calendar

class Dataset(Document):
  name = StringField()
  source_type = StringField()
  source_name = StringField()
  source_hostname = StringField()
  source_port = StringField()
  source_username = StringField()
  source_password = StringField()
  created = DateTimeField(default=datetime.datetime.utcnow)

  def __init__(self, name=None, source_type=None, source_name=None, source_hostname=None, source_port=None, source_username=None, source_password=None):
    self.name = name
    self.source_type = source_type
    self.source_name = source_name
    self.source_hostname = source_hostname
    self.source_port = source_port
    self.source_username = source_username
    self.source_password = source_password

  def __repr__(self):
    return "<Dataset('%s')>" str(self.id)

  def __unicode__(self):
    return self.__repr__()

  def to_serializable_object(self):
    return {
      'id': str(self.id),
      'name': self.name,
      'source_type' : self.source_type,
      'source_name' : self.source_name,
      'source_hostname' : self.source_hostname,
      'source_port' : self.source_port,
      'source_username' : self.source_username,
      'source_password' : self.source_password,
      'created': str(self.created),
    }

class DatasetData(Document):  
  dataset_id = StringField()
  custom_id = StringField()
  data = StringField()  

  dataset = ReferenceField('Dataset')

  meta = {
    'ordering' : ['dataset'],
    'indexes' : ['dataset'],
  }

  def __init__(self, dataset_id=None, custom_id=None, data=None):
    self.dataset_id = dataset_id
    self.custom_id = custom_id
    self.data = data
    
    #now reference the dataset
    d = Dataset.objects(id = dataset_id).first()
    self.dataset = d

  def __repr__(self):
    return 'DatasetData(%s)' % str(self.id)

  def __unicode__(self):
    return self.__repr__()

  def to_serializable_object(self):
    return {
      'id' : str(self.id),
      'dataset' : self.dataset_id,
      'custom_id' : self.custom_id,
      'data' : self.data,
    }
