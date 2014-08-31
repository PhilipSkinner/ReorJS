from base import ObjectBase

class Task(ObjectBase):
  __tablename__ = 'task'

  def __initattributes__(self):  
    self.id 			= self.Column('id', int, primary_key=True)
    self.owner 			= self.Column('owner', int, null=True)
    self.dataset_id 		= self.Column('dataset_id', int)    
    self.result_id 		= self.Column('result_id', int)
    self.application_id 	= self.Column('application_id', int)
    self.program 		= self.Column('program', str)
  
  def __repr__(self):
    return "<Task('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 		: str(self.id.value()),
      'owner' 		: self.owner.value(),
      'dataset' 	: self.dataset_id.value(),
      'result' 		: self.result_id.value(),
      'application' 	: self.application_id.value(),
      'program' 	: self.program.value(),
    }
