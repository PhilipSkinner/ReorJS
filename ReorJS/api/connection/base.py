"""
	api/connection/base.py
	Base connection class

	--
	Provides framework for creating an API database connection class.
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

import copy
import logger

class ConnectionBase():
	def __init__(self):
		logger.LOG.log("Connection initialization requires overriding for correct instantiation")

	def checkObject(self, object):
		logger.LOG.log("checkObject method requires overriding")

	def search(self, object, params={}, options={}):
		logger.LOG.log("search method requires overriding")

	def update(self, object):
		logger.LOG.log("update method requires overriding")

	def delete(self, object):
		logger.LOG.log("delete method requires overriding")

	def column(self, name, type, primary_key=False, null=False):
		return ColumnBase(name, type, primary_key=primary_key, null=null)

class ColumnBase():
	def __init__(self, name, type, primary_key=False, null=False):
		self._value = None
		self.name = name
		self.type = type

		self.null = null
		self.primary_key = primary_key

		if self.null and self.primary_key:
			logger.LOG.log("Column cannot be null and be primary key, fixing")
			self.null = False

		self.afterInit()

	def afterInit(self):
		return self

	def __set__(self):
		logger.LOG.log("__set__ method requires overriding")

		return None

	def __create__(self):
		logget.LOG.log("__create__ method requires overriding")

		return None

	def value(self, val=None):
		if val == None:
			return self._value

		if not self.primary_key:
			self._value=val

	def __value__(self, val):
		self._value = val
