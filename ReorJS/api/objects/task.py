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
    self.status			= self.Column('status', str)
    self.progress		= self.Column('progress', str)
    self.time_started		= self.Column('time_started', int)
    self.time_ended		= self.Column('time_ended', int)
    self.block_size		= self.Column('block_size', int)
    self.completion_cursor	= self.Column('completion_cursor', int)
  
  def __repr__(self):
    return "<Task('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 			: str(self.id.value()),
      'owner' 			: self.owner.value(),
      'dataset' 		: self.dataset_id.value(),
      'result' 			: self.result_id.value(),
      'application' 		: self.application_id.value(),
      'program' 		: self.program.value(),
      'status'			: self.status.value(),
      'progress'		: self.progress.value(),
      'time_started'		: self.time_started.value(),
      'time_ended'		: self.time_ended.value(),
      'block_size'		: self.block_size.value(),
      'completion_cursor' 	: self.completion_cursor.value(),      
    }
