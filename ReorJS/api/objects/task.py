from base import ObjectBase

class Task(ObjectBase):
  __tablename__ = 'task'

  def __initattributes__(self):  
    self.id 			= self.Column('id', int, primary_key=True)
    self.task 			= self.Column('task', int)
    self.owner 			= self.Column('owner', int)
    self.dataset_id 		= self.Column('dataset', int)
    self.result_id 		= self.Column('result', int)
    self.application_id 	= self.Column('application', int)
    self.program 		= self.Column('program', str)
  
  def __repr__(self):
    return "<Task('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 		: self.id,
      'task' 		: self.task,
      'owner' 		: self.owner,
      'dataset' 	: self.dataset_id,
      'result' 		: self.result_id,
      'application' 	: self.application_id,
      'program' 	: self.program,
    }
