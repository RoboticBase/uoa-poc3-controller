import os

import pytz

# environment variables
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE', 'UTC'))
ORION_ENDPOINT = os.environ['ORION_ENDPOINT']
FIWARE_SERVICE = os.environ['FIWARE_SERVICE']
FIWARE_SERVICEPATH = os.environ['FIWARE_SERVICEPATH']
ERROR_MARGIN = 8
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

# constants
ORION_BASE_PATH = '/v2/entities/'
ORION_LIST_NUM_LIMIT = 1000
ROBOT_TYPE = 'robot'
START_COMMAND = 'navi'

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]
