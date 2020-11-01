#!/usr/bin/env python
import json
import os
import logging.config
from logging import getLogger

from flask import Flask
from flask_cors import CORS

from src import api, const, errors

try:
    with open(const.LOGGING_JSON, "r") as f:
        logging.config.dictConfig(json.load(f))
        if (const.LOG_LEVEL in os.environ and
                os.environ[const.LOG_LEVEL].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            for handler in getLogger().handlers:
                if handler.get_name() in const.TARGET_HANDLERS:
                    handler.setLevel(getattr(logging, os.environ[const.LOG_LEVEL].upper()))
except FileNotFoundError:
    print(f'can not open {const.LOGGING_JSON}')
    pass

app = Flask(__name__)
if const.CORS_ORIGINS:
    CORS(app, resources={r'/*': {'origins': const.CORS_ORIGINS}})
app.config.from_pyfile('config.cfg')

planner = api.StaticRoutePlanner.as_view(api.StaticRoutePlanner.NAME)
app.add_url_rule('/api/v1/planning', view_func=planner, methods=['POST', ])

app.register_blueprint(errors.app)


if __name__ == '__main__':
    default_port = app.config['DEFAULT_PORT']
    try:
        port = int(os.environ.get(const.LISTEN_PORT, str(default_port)))
        if port < 1 or 65535 < port:
            port = default_port
    except ValueError:
        port = default_port
    app.run(host='0.0.0.0', port=port)
