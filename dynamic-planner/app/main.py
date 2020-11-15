#!/usr/bin/env python
import json
import os
import logging.config
from logging import getLogger
from importlib import import_module
from queue import Queue

from flask import Flask

from src import api, const, errors
from src.potential import Potential

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
app.config.from_pyfile('config.cfg')

graph_generator = api.GraphGenerator.as_view(api.GraphGenerator.NAME)
app.add_url_rule('/api/v1/graph/', view_func=graph_generator, methods=['POST', ])

try:
    graph = import_module(const.GRAPH_MODULE)
    size = graph.SIZE
    nodes = graph.NODES
    edges = graph.EDGES
    for node in nodes.values():
        node.edges = [edge for edge in edges if edge.st == node or edge.ed == node]

    potential = Potential(size)
    req_queue = Queue()
    state_holder = dict()
    plan_holder = dict()

    planner = api.DynamicRoutePlanner.as_view(api.DynamicRoutePlanner.NAME,
                                              potential, req_queue, plan_holder, size, nodes, edges)
    potential_viewer = api.PotentialViewer.as_view(api.PotentialViewer.NAME, potential, size, nodes, edges)
    pose_notifiee = api.PoseNotifiee.as_view(api.PoseNotifiee.NAME, potential)
    mode_notifiee = api.ModeNotifiee.as_view(api.ModeNotifiee.NAME, potential, state_holder)
    graph_viewer = api.GraphViewer.as_view(api.GraphViewer.NAME, size, nodes, edges)
    app.add_url_rule('/api/v1/plans/', defaults={'plan_id': None}, view_func=planner, methods=['GET', 'POST', ])
    app.add_url_rule('/api/v1/plans/<plan_id>', view_func=planner, methods=['GET', 'DELETE', ])
    app.add_url_rule('/api/v1/potentials/', view_func=potential_viewer, methods=['GET', ])
    app.add_url_rule('/api/v1/notifications/pose', view_func=pose_notifiee, methods=['POST', ])
    app.add_url_rule('/api/v1/notifications/mode', view_func=mode_notifiee, methods=['POST', ])
    app.add_url_rule('/api/v1/graph/', view_func=graph_viewer, methods=['GET', ])
except ModuleNotFoundError:
    print(f'can not load {const.GRAPH_MODULE}')
    pass

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
