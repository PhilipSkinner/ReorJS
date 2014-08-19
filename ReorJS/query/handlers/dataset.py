from base import *
import api

class APIDataSetHandler(BaseHandler):
  def get(self, id=None):  
    if id == None:
      results = api.db.Dataset.search({})
      
      self.payload([r.to_serializable_object() for r in results])
      return
    else:
      dataset = api.db.Dataset.find({ 'id' : id })
      
      if dataset == None:
        self.error('2001', 'Dataset %s not found' % id)
        return
      
      self.payload(dataset.to_serializable_object())
      return
  
  def post(self, id=None):
    name = self.get_argument('name', None)
    
    if name == None or name.replace(' ', '') == '':
      self.error('2002', 'Dataset requires a name')
      return
    
    if id == None:
      dataset = api.db.Dataset.create({ 'name' : name })
      dataset.update()
      
      self.status('200', 'Dataset successfully created')
      return
    else:
      dataset = api.db.Dataset.find({ 'id' : id })
      
      if dataset == None:
        self.error('2001', 'Dataset %d not found' % id)
        return
      
      dataset.name.value(name)
      dataset.update()
      
      self.status('200', 'Dataset %s updated successfully' % id)
      return
  
  def put(self, id=None):
    self.post(id=id)
  
  def delete(self, id=None):
    if id == None:
      self.error('2003', 'Cannot delete dataset without a dataset id')
      return
    
    dataset = api.db.Dataset.find({ 'id' : id })
    
    if dataset == None:
      self.error('2001', 'Dataset %s not found' % id)
      return
    
    dataset.delete()
    
    self.status('200', 'Dataset %d deleted successfully' % id)
    return

class APIDataSetDataHandler(BaseHandler):
  def get(self, id=None):
    if id == None:
      self.error('2004', 'Dataset data fetching requires dataset id')
      return
    
    results = api.db.DatasetData.search({ 'dataset' : id })
    
    self.payload([r.to_serializable_object() for r in results])
    return
  
  def post(self, id=None):
    items = self.get_arguments('data', [])
    
    if len(items) == 0 or items == None:
      self.error('2005', 'Data must be provided for insertion')
      return
    
    dataset = api.db.Dataset.find({ 'id' : id })
    
    if dataset == None:
      self.error('2001', 'Dataset %s not found' % id)
      return
    
    count = 0;
    for point in items:
      temp = api.db.DatasetData.create({ 'dataset' : id, 'data' : point, 'custom_id' : '' })
      temp.update()
      count += 1
      
    self.status('200', '%d datapoints added to dataset %s' % (count, id))
    return

