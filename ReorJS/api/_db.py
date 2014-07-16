import settings

class APIDB():
	def __init__(self):
		#just setup our values for later		
		self.connection = None
	
	def connect(self):
		if settings.DB_TYPE == 'redis':
			print "Configuring for redis"
		elif settings.DB_TYPE == 'mysql':
			print "Configuring for mysql"
			
			import mysql
			
			mysql.Session(username=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, name=settings.MYSQL_NAME)
			
		elif settings.DB_TYPE == 'mongo':
			print "Configuring for mongo"
			
			import mongo
			import pymongo
			import pymongo.collection
			
			mongo.connection = mongo.connect(settings.MONGO_NAME, host=settings.MONGO_HOST, port=int(settings.MONGO_PORT), read_preference=settings.MONGO_READ)
			mongo.rawConnection = pymongo.MongoClient(settings.MONGO_HOST, int(settings.MONGO_PORT))
			
