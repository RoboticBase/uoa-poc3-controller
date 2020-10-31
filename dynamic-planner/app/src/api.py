import datetime
import io
import json
import threading
import time
from textwrap import dedent

from logging import getLogger

from flask import jsonify, request, abort, make_response
from flask.views import MethodView

from PIL import Image

from src import const, orion
from src.fast_astar import FastAstar
from src.grid_generator import Grid
from src.data import ReqState, Req, Mode, State, Node

logger = getLogger(__name__)


class DynamicRoutePlanner(MethodView):
    NAME = 'dynamic_route_planner'

    def __init__(self, potential, req_queue, graph_size, nodes, edges):
        super().__init__()
        self.potential = potential
        self.req_queue = req_queue
        self.graph_size = graph_size
        self.nodes = nodes
        self.edges = edges
        threading.Thread(target=self._exec).start()

    def post(self):
        logger.debug('DynamicRoutePlanner.post')
        body = request.json

        if body is None or body.get('robotId') is None or body.get('startNode') is None or body.get('destNode') is None:
            msg = f'"robotId" and/or "startNode" and/or "destNode" do not exist, body={body}'
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })

        robot_id = body['robotId']
        start_node = body['startNode']
        dest_node = body['destNode']
        dest_angle = body.get('destAngle')

        if self.potential.has_potential(robot_id):
            msg = f'this robot ({robot_id}) already has potential'
            logger.warning(f'status=409, {msg}')
            return jsonify({
                'result': 'failure',
                'message': msg,
            }), 409

        entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id)
        if 'robotSize' not in entity or 'inflation_radius' not in entity['robotSize']['value']:
            msg = f'the "robotSize" of {robot_id} has not been initialized yet.' \
                  f'use default inflation_radius ({const.DEFAULT_INFLATION_RADIUS})'
            logger.warning(f'{msg}')
            inflation_radius = const.DEFAULT_INFLATION_RADIUS
        else:
            inflation_radius = float(entity['robotSize']['value']['inflation_radius'])

        req = Req(robot_id, start_node, dest_node, dest_angle, inflation_radius)
        self.req_queue.put(req)

        msg = f'enqueued this request, {req}'
        logger.info(f'status=200, {msg}')
        return jsonify({
            'result': 'success',
            'message': msg,
        })

    def _exec(self):
        while True:
            req = self.req_queue.get()
            logger.debug(f'DynamicRoutePlanner._exec, queue_length={self.req_queue.qsize()} req={req}')
            if req.state == ReqState.RETRY:
                time.sleep(const.RETRY_QUEUE_WAIT_SEC)

            radius = req.inflation_radius/float(const.COSTMAP_METADATA['resolution'])

            fast_astar = FastAstar(
                self.nodes[req.start_node],
                self.nodes[req.dest_node],
                list(self.nodes.values()),
                self.graph_size,
                radius)

            searched_path = fast_astar.calculate(self.potential.current_field)

            if not searched_path:
                req.state = ReqState.RETRY
                self.req_queue.put(req)
                continue

            self.potential.register(req.robot_id, searched_path, radius)

            payload = self._make_cmd(req.inflation_radius, searched_path, req.dest_angle)

            result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, req.robot_id, payload)
            logger.info(f'send a "{const.START_COMMAND}" command to orion, '
                        f'result_status={result.status_code}, payload={json.dumps(payload)}')

    def _make_cmd(self, inflation_radius, waypoints, dest_angle):
        t = datetime.datetime.now(const.TIMEZONE).isoformat(timespec='milliseconds')

        payload = {
            'naviCmd': {
                'type': 'command',
                'value': {
                    'time': t,
                    'command': const.START_COMMAND,
                    'metadata': {
                        'inflation_radius': inflation_radius,
                        'costmap': const.COSTMAP_METADATA,
                    },
                    'waypoints': [{
                        'point': {
                            'x': n.x,
                            'y': n.y,
                            'z': 0.0,
                        },
                        'angle': None,
                    } for n in waypoints],
                    'destination': {
                        'point': {
                            'x': waypoints[-1].c_x,
                            'y': waypoints[-1].c_y,
                            'z': 0.0,
                        },
                        'angle': {
                            'roll': 0.0,
                            'pitch': 0.0,
                            'yaw': dest_angle,
                        } if dest_angle is not None else None
                    }
                }
            }
        }
        return payload


class PotentialViewer(MethodView):
    NAME = 'potential_viewer'

    def __init__(self, potential):
        super().__init__()
        self.potential = potential

    def get(self):
        logger.debug('PotentialViewer.get')

        output = io.BytesIO()
        Image.fromarray(self.potential.current_field).save(output, format='JPEG')

        response = make_response()
        response.data = output.getvalue()
        response.mimetype = 'image/jpeg'

        return response


class PoseNotifiee(MethodView):
    NAME = 'pose_notifiee'

    def __init__(self, potential):
        super().__init__()
        self.potential = potential

    def post(self):
        logger.debug('PoseNotifiee.post')

        passed = None
        for data in request.json.get('data', []):
            if 'id' in data and 'pose' in data and 'point' in data['pose']['value']:
                robot_id = data['id']
                c_x = data['pose']['value']['point']['x']
                c_y = data['pose']['value']['point']['y']
                if 'robotSize' not in data or 'inflation_radius' not in data['robotSize']['value']:
                    inflation_radius = const.DEFAULT_INFLATION_RADIUS
                else:
                    inflation_radius = float(data['robotSize']['value']['inflation_radius'])
                passed = self.potential.notify_pos(robot_id, c_x, c_y, inflation_radius)
                logger.info(f'passed waypoints = {passed}')

        return jsonify({'result': 'success', 'passedWaypointNum': 0 if passed is None else len(passed)}), 200


class ModeNotifiee(MethodView):
    NAME = 'mode_notifiee'

    def __init__(self, potential, state_holder):
        super().__init__()
        self.potential = potential
        self.state_holder = state_holder

    def post(self):
        logger.debug('ModeNotifee.post')

        for data in request.json.get('data', []):
            if 'id' in data and 'mode' in data:
                robot_id = data['id']
                if robot_id not in self.state_holder:
                    self.state_holder[robot_id] = State()

                updated = self.state_holder[robot_id].update(data['mode']['value'])
                logger.debug(f'state = {self.state_holder[robot_id]}')
                if updated and self.state_holder[robot_id].current_mode == Mode.STANDBY:
                    self.potential.deregister(robot_id)
                    logger.debug(f'deregister potential of {robot_id}')

        return jsonify({'result': 'success'}), 200


class GraphGenerator(MethodView):
    NAME = 'graph_generator'

    TEMPLATE = """
    from src.data import Node, Edge

    SIZE = {size}

    NODES = {nodes}

    EDGES = {edges}
    """

    def post(self):
        if 'map_pgm' not in request.files:
            msg = 'map_pgm does not exist'
            logger.warning(msg)
            return jsonify({
                'result': 'failure',
                'message': msg,
            }), 400
        map_pgm = request.files['map_pgm']

        if 'metadata_json' not in request.files:
            msg = 'yaml_file does not exist'
            logger.warning(msg)
            return jsonify({
                'result': 'failure',
                'message': msg,
            }), 400
        metadata_json = request.files['metadata_json']

        u_length_m = float(request.form['u_length_m']) if 'u_length_m' in request.form else const.DEFAULT_UNIT_LENGTH

        grid = Grid(map_pgm, metadata_json, u_length_m)
        graph = grid.build_graph()

        nodes = {f'N{i:04}': Node(x=vertex.pixel[0], y=vertex.pixel[1], c_x=vertex.converted[0], c_y=vertex.converted[1])
                 for i, vertex in enumerate(graph.keys())}

        raw_edges = list()
        for current, neighbors in graph.items():
            for neighbor in neighbors:
                raw_edges.append(tuple(sorted((current, neighbor))))

        edges = list()
        for e in set(raw_edges):
            edges.append(f'Edge(NODES["{self.find_node(nodes, e[0])[0]}"], NODES["{self.find_node(nodes, e[1])[0]}"])')

        response = make_response()
        response.data = dedent(GraphGenerator.TEMPLATE.format(size=grid.size, nodes=nodes, edges=f'[{",".join(edges)}]'))
        response.mimetype = 'text/plain'

        return response

    def find_node(self, nodes, v):
        return next(((k, n) for k, n in nodes.items()
                    if n.x == v.pixel[0] and n.y == v.pixel[1] and n.c_x == v.converted[0] and n.c_y == v.converted[1]))
