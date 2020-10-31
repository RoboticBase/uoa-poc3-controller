import os

import pytz

# environment variables
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE', 'UTC'))
ORION_ENDPOINT = os.environ['ORION_ENDPOINT']
FIWARE_SERVICE = os.environ['FIWARE_SERVICE']
FIWARE_SERVICEPATH = os.environ['FIWARE_SERVICEPATH']
ERROR_MARGIN = 1.1
CHECK_WP_LENGTH = 3
GRAPH_MODULE = 'graph.lictia'
COSTMAP_METADATA = {
    "resolution": 0.05,
    "width": 749,
    "height": 531,
    "origin": {
        "point": {
            "x": -19.3,
            "y": -20,
            "z": 0
        },
        "angle": {
            "roll": 0,
            "pitch": 0,
            "yaw": 0
        }
    }
}
MODE_CHANGE_COUNT = 3
RETRY_QUEUE_WAIT_SEC = 1

# constants
ORION_BASE_PATH = '/v2/entities/'
ORION_LIST_NUM_LIMIT = 1000
ROBOT_TYPE = 'robot'
START_COMMAND = 'navi'
MODE_NAVI = 'navi'
MODE_STAQNDBY = 'standby'
MODE_ERROR = 'error'
MODE_UNKNOWN = 'unknown'
DEFAULT_INFLATION_RADIUS = 0.5

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]
