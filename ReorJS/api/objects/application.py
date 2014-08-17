from base import ObjectBase

class Application(ObjectBase):
  __tablename__ = 'application'

  def __initattributes__(self):  
    self.id 		= self.Column('id', int, primary_key=True)
    self.name		= self.Column('name', str)
    self.program 	= self.Column('program', str)
  
  def __repr__(self):
    return "<Application('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 		: self.id,
      'name' 		: self.name,
      'program' 	: self.program,
    }
