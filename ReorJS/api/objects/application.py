from base import ObjectBase

class Application(ObjectBase):
  __tablename__ = 'application'

  def __initattributes__(self):  
    self.id 		= self.Column('id', int, primary_key=True)
    self.name		= self.Column('name', str)
    self.program 	= self.Column('program', str)
    
    self.__attributes__ = True
  
  def __repr__(self):    
    return "<Application>"
  
  def to_serializable_object(self):
    return {
      'id' 		: str(self.id.value()),
      'name' 		: self.name.value(),
      'program' 	: self.program.value(),
    }
