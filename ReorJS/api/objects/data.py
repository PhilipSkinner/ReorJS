from base import ObjectBase

class Dataset(ObjectBase):
  __tablename__ = 'dataset'

  def __initattributes__(self):
    self.id 			= self.Column('id', int, primary_key=True)
    self.name 			= self.Column('name', str)
    self.source_type 		= self.Column('source_type', str)
    self.source_name 		= self.Column('source_name', str)
    self.source_hostname 	= self.Column('source_hostname', str)
    self.source_port 		= self.Column('source_port', str)
    self.source_username 	= self.Column('source_username', str)
    self.source_password 	= self.Column('source_password', str)
    self.source_table		= self.Column('source_table', str)
    self.created 		= self.Column('created', str)

  def __repr__(self):
    return "<Dataset('%s')>" % self.id
    
  def to_serializable_object(self):
    return {
      'id' 		: self.id,
      'name' 		: self.name,
      'source_type' 	: self.source_type,
      'source_name' 	: self.source_name,
      'source_hostname' : self.source_hostname,
      'source_port' 	: self.source_port,
      'source_username' : self.source_username,
      'source_password' : self.source_password,
      'source_table'	: self.source_table.value(),
      'created' 	: str(self.created),
    }

class DatasetData(ObjectBase):
  __tablename__ = 'dataset_data'
  
  def __initattributes__(self):
    self.id 			= self.Column('id', int, primary_key=True)
    self.dataset_id 		= self.Column('dataset', int)
    self.custom_id 		= self.Column('custom_id', str)
    self.data 			= self.Column('data', str)
  
  def __repr__(self):
    return "<DatasetData('%s')>" % self.id

  def to_serializable_object(self):
    return {
      'id' 		: self.id,
      'dataset' 	: self.dataset_id,
      'custom_id' 	: self.custom_id,
      'data' 		: self.data,
    }
  
