from base import BaseQueryService
import settings
import logger

class QueryBaseHTTPServer(BaseQueryService):
	def __init__(self):
		logger.LOG.log("Setting up QueryBaseHTTPServer")

