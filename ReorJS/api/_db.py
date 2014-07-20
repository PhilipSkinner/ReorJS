import settings

class APIDB():
	def __init__(self):
		#just setup our values for later		
		self.connection = None
		self.type = None
	
	def connect(self):
		self.type = settings.DB_TYPE
		if settings.DB_TYPE == 'redis':
			print "Configuring for redis"
		elif settings.DB_TYPE == 'mysql':
			print "Configuring for mysql"
			
			try:
				import mysql								
			
				mysql.Session(username=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, name=settings.MYSQL_NAME)
			except:
				return False
			
		elif settings.DB_TYPE == 'mongo':
			print "Configuring for mongo"
			
			try:
				import mongo
				import pymongo
				import pymongo.collection
			
				mongo.connection = mongo.connect(settings.MONGO_NAME, host=settings.MONGO_HOST, port=int(settings.MONGO_PORT), read_preference=settings.MONGO_READ)
				mongo.rawConnection = pymongo.MongoClient(settings.MONGO_HOST, int(settings.MONGO_PORT))
			except:
				return False
		
		return True
			

	def query(self, type, args=None):
		if self.type == 'redis':
			print "Running query on redis"
		elif self.type == 'mysql':
			print "Running query on mysql"
			try:
				import mysql
				
				filters = []
				if args != None:
					for k, v in args.iter_items():
						filters.append('%s == %s' % (k, v))	
				
				result = mysql.session.query(type).filter(filters)
			except:
				return None
		elif self.type == 'mongo':
			print "Running query on mongo"
