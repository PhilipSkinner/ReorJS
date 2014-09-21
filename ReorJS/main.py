import conf
import settings
import api
import query
import stack
import output
import input
import logger

def main():
	config = conf.configure()
	
	#now configure our settings global
	set_setting('LOG_LOCATION',		config.log_location)
	set_setting('DEBUG', 			config.debug)
	set_setting('VERBOSE', 			config.verbose)

	#init logging
	logger.initLogger()

	set_setting('REGISTRATION_HOST', 	config.reg_host)
	set_setting('REGISTRATION_PORT', 	config.reg_port)
	set_setting('PORT', 			config.port)
	set_setting('IP', 			config.ip)
	set_setting('DB_TYPE', 			config.db_type)
	set_setting('REDIS_SOCKET', 		config.redis_sock)
	set_setting('REDIS_HOST', 		config.redis_host)
	set_setting('REDIS_PORT', 		config.redis_port)
	set_setting('MONGO_NAME',		config.mongo_name)
	set_setting('MONGO_HOST',		config.mongo_host)
	set_setting('MONGO_PORT',		config.mongo_port)
	set_setting('MONGO_READ',		config.mongo_read)
	set_setting('MYSQL_NAME',		config.mysql_name)
	set_setting('MYSQL_HOST',		config.mysql_host)
	set_setting('MYSQL_PORT',		config.mysql_port)
	set_setting('MYSQL_USER',		config.mysql_user)
	set_setting('MYSQL_PASSWORD',		config.mysql_password)
	set_setting('HTTP_SERVICE',		config.server)

	logger.LOG.log('ReorJS service starting...')
	logger.LOG.log('Initializing API')
	logger.LOG.info('Starting with the following settings:')
	logger.LOG.info('LOG_LOCATION		=> %s' % settings.LOG_LOCATION)
	logger.LOG.info('DEBUG			=> %s' % settings.DEBUG)
	logger.LOG.info('VERBOSE			=> %s' % settings.VERBOSE)
	logger.LOG.info('REGISTRATION_HOST	=> %s' % settings.REGISTRATION_HOST)
	logger.LOG.info('REGISTRATION_PORT	=> %s' % settings.REGISTRATION_PORT)
	logger.LOG.info('PORT			=> %s' % settings.PORT)
	logger.LOG.info('IP			=> %s' % settings.IP)
	logger.LOG.info('DB_TYPE			=> %s' % settings.DB_TYPE)
	logger.LOG.info('REDIS_SOCKET		=> %s' % settings.REDIS_SOCKET)
	logger.LOG.info('REDIS_HOST		=> %s' % settings.REDIS_HOST)
	logger.LOG.info('REDIS_PORT		=> %s' % settings.REDIS_PORT)
	logger.LOG.info('MONGO_NAME		=> %s' % settings.MONGO_NAME)
	logger.LOG.info('MONGO_HOST		=> %s' % settings.MONGO_HOST)
	logger.LOG.info('MONGO_PORT		=> %s' % settings.MONGO_PORT)
	logger.LOG.info('MONGO_READ		=> %s' % settings.MONGO_READ)
	logger.LOG.info('MYSQL_NAME		=> %s' % settings.MYSQL_NAME)
	logger.LOG.info('MYSQL_HOST		=> %s' % settings.MYSQL_HOST)
	logger.LOG.info('MYSQL_PORT		=> %s' % settings.MYSQL_PORT)
	logger.LOG.info('MYSQL_USER		=> %s' % settings.MYSQL_USER)
	logger.LOG.info('MYSQL_PASSWORD		=> %s' % settings.MYSQL_PASSWORD)
	logger.LOG.info('HTTP_SERVICE		=> %s' % settings.HTTP_SERVICE)
	
	#we need to configure our API database from settings
	if api.connect():	
		#and then our stacker		
		logger.LOG.log('Initializing stacker')
		stack.initStacker()
		
		#next we need to create our query service
		logger.LOG.log('Initializing query service')
		service = query.QueryService()
		
		#and run it
		logger.LOG.log('Running service...')
		service.run()		
	else:
		logger.LOG.log("Error connecting to API database, please check configuration.")
	

def set_setting(name, value):
	if settings.VERBOSE:
		logger.LOG.log('Setting system variable %s to value %s' % (name, value))
		
	setattr(settings, name, value)
	
def sigHandler(signal, frame):
	logger.LOG.log('ReorJS service exiting')	
	sys.exit(0)

if __name__ == '__main__':
	main()
