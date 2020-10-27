import os

# environment variables
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
ORION_ENDPOINT = os.environ['ORION_ENDPOINT']
FIWARE_SERVICE = os.environ['FIWARE_SERVICE']
FIWARE_SERVICEPATH = os.environ['FIWARE_SERVICEPATH']

# constants
ORION_BASE_PATH = '/v2/entities/'
ORION_LIST_NUM_LIMIT = 1000
PLAN_TYPE = 'plan'

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]
