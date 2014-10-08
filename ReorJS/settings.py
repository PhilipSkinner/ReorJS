"""
        settings.py
        ReorJSd settings
        
        --
        Module for storage of the ReorJSd internal settings.
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

import os

#global values for use in the application

#logging
LOG_LOCATION = '/var/log/reorjs'

#debug mode
DEBUG = False
VERBOSE = False

#base directory
BASE_PATH = os.path.dirname(__file__)

#registration values
REGISTRATION_HOST = None
REGISTRATION_PORT = None

#service values
PORT = None
IP = None
HTTP_SERVICE = None

#database type
DB_TYPE = None

#redis settings
REDIS_SOCKET = None
REDIS_HOST = None
REDIS_PORT = None

#mongo settings
MONGO_NAME = None
MONGO_HOST = None
MONGO_PORT = None
MONGO_READ = None

#mysql settings
MYSQL_NAME = None
MYSQL_HOST = None
MYSQL_PORT = None
MYSQL_USER = None
MYSQL_PASSWORD = None

#stacker settings
BLOCKSIZE = 25
TASKLIMIT = 15
READMETHOD = 1
