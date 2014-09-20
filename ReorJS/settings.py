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
BLOCKSIZE = 100
