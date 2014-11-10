"""
	api/_db.py
	ReorJSd API DB connection manager

	--
	Manages which backend DB to use for the ReorJSd API database.
	--

	Author(s)       - Philip Skinner (philip@crowdca.lc)
	Last modified   - 2014-09-28

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

	Copyright (c) 2014, Crowdcalc B.V.
"""

import settings
import logger
from .objects.application import Application
from .objects.data import Dataset
from .objects.data import DatasetData
from .objects.stacker import Stacker
from .objects.task import Task
from .objects.key import Key

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
		self.Key		= Key(parent=self, init=True)

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
				import pymysql as mdb

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
				from .connection import mysql
				self._connection = mysql.Connection(self.dbconnection)
			except:
				return False

		elif settings.DB_TYPE == 'mongo':
			logger.LOG.log("Configuring for mongo")

			try:
				from .connection import mongo
				self._connection = mongo.Connection(self.dbconnection)
			except:
				return False

		return self._connection != None
