from base import ObjectBase

class Stacker(ObjectBase):
  __tablename__ = 'stacker'

  def __initattributes__(self):  
    self.id 			= self.Column('id', int, primary_key=True)
    self.ip 			= self.Column('ip', str)
    self.port 			= self.Column('port', int)
    self.status 		= self.Column('status', int)
  
  def __repr__(self):
    return "<Stacker('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 		: self.id,
      'ip' 		: self.ip,
      'port' 		: self.port,
      'status' 		: self.status,
    }
