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
      'id' 		: str(self.id.value()),
      'task' 		: self.task.value(),
      'owner' 		: self.owner.value(),
      'dataset' 	: self.dataset_id.value(),
      'result' 		: self.result_id.value(),
      'application' 	: self.application_id.value(),
      'program' 	: self.program.value(),
    }
