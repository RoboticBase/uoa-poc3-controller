import os
import json

import pytz

# environment variables
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE', 'UTC'))
ORION_ENDPOINT = os.environ['ORION_ENDPOINT']
FIWARE_SERVICE = os.environ['FIWARE_SERVICE']
FIWARE_SERVICEPATH = os.environ['FIWARE_SERVICEPATH']
GRAPH_MODULE = os.environ['GRAPH_MODULE']
COSTMAP_METADATA = json.loads(os.environ['COSTMAP_METADATA'])
ERROR_MARGIN = float(os.environ.get('ERROR_MARGIN', '1.1'))
CHECK_WP_LENGTH = int(os.environ.get('CHECK_WP_LENGTH', '3'))
MODE_CHANGE_COUNT = int(os.environ.get('MODE_CHANGE_COUNT', '3'))
RETRY_QUEUE_WAIT_SEC = int(os.environ.get('RETRY_QUEUE_QAIT_SEC', '1'))
GRAPH_MULTIPLY = int(os.environ.get('GRAPH_MULTIPLY', '3'))
ROBOT_TYPE = os.environ.get('ROBOT_TYPE', 'robot')

# constants
ORION_BASE_PATH = '/v2/entities/'
ORION_LIST_NUM_LIMIT = 1000
START_COMMAND = 'navi'
MODE_NAVI = 'navi'
MODE_STAQNDBY = 'standby'
MODE_ERROR = 'error'
MODE_UNKNOWN = 'unknown'
DEFAULT_INFLATION_RADIUS = 0.4
DEFAULT_UNIT_LENGTH = 0.8
POS_POSTFIX = '_pos'
NODE_NAME_LENGTH = 5

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]
