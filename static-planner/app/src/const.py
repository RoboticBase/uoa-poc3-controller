import os

import pytz

# environment variables
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE', 'UTC'))
ORION_ENDPOINT = os.environ['ORION_ENDPOINT']
FIWARE_SERVICE = os.environ['FIWARE_SERVICE']
FIWARE_SERVICEPATH = os.environ['FIWARE_SERVICEPATH']
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', None)

# constants
ORION_BASE_PATH = '/v2/entities/'
ORION_LIST_NUM_LIMIT = 1000
PLAN_TYPE = 'plan'
ROBOT_TYPE = 'robot'
START_COMMAND = 'start'

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]
