import settings
import logger
from objects.application import Application
from objects.data import Dataset
from objects.data import DatasetData
from objects.stacker import Stacker
from objects.task import Task

class APIDB():
	Application 	= None
	Dataset 	= None
	DatasetData 	= None
	Stacker 	= None
	Task 		= None

	def __init__(self):
		#just setup our values for later		
		self._connection = None
		self._dbconnection = None
		self.type = None
		self.ready = False
		
		#and connect
		if not self.connect():
			logger.LOG.log("Could not connect to API datasource")
			return None

		#object accessors
		self.Application 	= Application(parent=self, init=True)
		self.Dataset 		= Dataset(parent=self, init=True)
		self.DatasetData 	= DatasetData(parent=self, init=True)
		self.Stacker 		= Stacker(parent=self, init=True)
		self.Task		= Task(parent=self, init=True)		
		
		self.ready = True
		
	def connection(self):
		if self._connection == None:
			self.connect()
			
		return self._connection
		
	def dbconnection(self):
		if self._dbconnection == None:
			self.dbconnect()
		else:
			s = '%s' % self._dbconnection
			try:
				i = s.index('closed')
				if i != None:
					self.dbconnect()
			except:
				pass
			
		return self._dbconnection
	
	def dbconnect(self):
		if settings.DB_TYPE == 'redis':
			logger.LOG.log("Connecting to redis")
		elif settings.DB_TYPE == 'mysql':
			logger.LOG.log("Connecting to mysql")
			
			try:
				import MySQLdb as mdb
				
				self._dbconnection = mdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_NAME)
			except:
				pass
		elif settings.DB_TYPE == 'mongo':
			logger.LOG.log("Connecting to mongo")
			
			try:
				import pymongo
			
				self._dbconnection = pymongo.MongoClient(settings.MONGO_HOST, int(settings.MONGO_PORT))
			except:
				pass
		
		
	def connect(self):
		logger.LOG.log("Attempting API datasource (%s) connection..." % settings.DB_TYPE)
	
		self.type = settings.DB_TYPE
		if settings.DB_TYPE == 'redis':
			logger.LOG.log("Configuring for redis")
		elif settings.DB_TYPE == 'mysql':
			logger.LOG.log("Configuring for mysql")

			try:
				import connection.mysql as mysql
				
				self._connection = mysql.Connection(self.dbconnection)
			except:
				return False
			
		elif settings.DB_TYPE == 'mongo':
			logger.LOG.log("Configuring for mongo")

			try:
				import connection.mongo as mongo
			
				self._connection = mongo.Connection(self.dbconnection)
			except:
				return False
		
		return self._connection != None
