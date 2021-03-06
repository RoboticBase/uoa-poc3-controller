import datetime
import io
import json
import math
import threading
import time
from textwrap import dedent

from logging import getLogger

from flask import jsonify, request, abort, make_response
from flask.views import MethodView

import numpy as np

from PIL import Image, ImageDraw

from src import const, orion
from src.fast_astar import FastAstar
from src.grid_generator import Grid
from src.data import ReqState, Req, Mode, State, Node, Edge

logger = getLogger(__name__)


class DynamicRoutePlanner(MethodView):
    NAME = 'dynamic_route_planner'

    def __init__(self, potential, req_queue, plan_holder, graph_size, nodes, edges):
        super().__init__()
        self.potential = potential
        self.req_queue = req_queue
        self.plan_holder = plan_holder
        self.graph_size = graph_size
        self.nodes = nodes
        self.edges = edges
        threading.Thread(target=self._exec).start()

    def get(self, plan_id):
        logger.debug(f'DynamicRoutePlanner.get, plan_id={plan_id}')
        if plan_id is None:
            return jsonify([req.json for req in self.plan_holder.values()])

        if self.plan_holder.get(plan_id):
            return jsonify(self.plan_holder[plan_id].json)

        abort(404, {
            'result': 'failure',
            'message': f'plan ({plan_id}) does not found',
        })

    def delete(self, plan_id):
        logger.debug(f'DynamicRoutePlanner.delete, plan_id={plan_id}')

        if plan_id is None or not self.plan_holder.get(plan_id):
            abort(404, {
                'result': 'failure',
                'message': f'plan ({plan_id}) does not found',
            })

        if self.plan_holder[plan_id].state in (ReqState.DONE, ReqState.DELETE):
            abort(409, {
                'result': 'failure',
                'message': f'plan ({plan_id}) has already been done or deleted',
            })

        self.plan_holder[plan_id].state = ReqState.DELETE
        return make_response('', 204)

    def post(self, **kwargs):
        logger.debug('DynamicRoutePlanner.post')
        body = request.json

        if body is None or body.get('robotId') is None or body.get('destNode') is None:
            msg = f"'robotId' and/or 'destNode' do not exist (optional 'startNode', 'destAngle'), body={body}"
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })

        robot_id = body['robotId']
        start_node = body.get('startNode')
        dest_node = body['destNode']
        dest_angle = body.get('destAngle')

        if not isinstance(robot_id, str):
            msg = f"'robotId' is not str, robotId={robot_id}"
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })
        if start_node is not None and not self.nodes.get(start_node):
            msg = f"'startNode' does not exist, destNode={start_node}"
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })
        if not self.nodes.get(dest_node):
            msg = f"'destNode' does not exist, destNode={dest_node}"
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })
        if dest_angle is not None and not isinstance(dest_angle, (int, float)):
            msg = f"'destAngle' is not number, destAngle={dest_angle}"
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })

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
        self.plan_holder[req.id] = req
        self.req_queue.put(req)

        logger.info(f'status=200, enqueued request = {req}')
        return jsonify({
            'result': 'success',
            'enqueued': req.json,
        })

    def _exec(self):
        while True:
            req = self.req_queue.get()
            logger.debug(f'DynamicRoutePlanner._exec get queue ,req={req}')
            if req.state == ReqState.RETRY:
                time.sleep(const.RETRY_QUEUE_WAIT_SEC)

            if req.state == ReqState.DELETE:
                logger.debug(f'DynamicRoutePlanner._exec delete queue ,req={req}')
                continue

            radius = req.inflation_radius/float(const.COSTMAP_METADATA['resolution'])

            entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, req.robot_id)
            start_node = self._calc_start_node(entity, req.start_node)

            if not start_node:
                if req.state != ReqState.DELETE:
                    logger.debug(f'DynamicRoutePlanner._exec reput queue ,req={req}')
                    req.state = ReqState.RETRY
                    self.req_queue.put(req)
                continue

            fast_astar = FastAstar(
                self.nodes[start_node],
                self.nodes[req.dest_node],
                list(self.nodes.values()),
                self.graph_size,
                radius)

            ignore_id = f'{req.robot_id}{const.POS_POSTFIX}'
            searched_path = fast_astar.calculate(self.potential.get_current_field(ignore_id=ignore_id))

            if not searched_path:
                if req.state != ReqState.DELETE:
                    logger.debug(f'DynamicRoutePlanner._exec reput queue ,req={req}')
                    req.state = ReqState.RETRY
                    self.req_queue.put(req)
                continue

            total_path = self._connect_current_point(entity, searched_path)

            self.potential.register(req.robot_id, total_path, radius)

            payload = self._make_cmd(req.inflation_radius, total_path, req.dest_angle)

            result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, req.robot_id, payload)
            req.state = ReqState.DONE
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

    def _calc_start_node(self, entity, start_node):
        if start_node is not None:
            return start_node

        if 'pose' not in entity or 'point' not in entity['pose']['value']:
            return None

        point = entity['pose']['value']['point']
        return self._find_nearest_node(point['x'], point['y'])

    def _find_nearest_node(self, c_x, c_y):
        dtype = [('name', f'U{const.NODE_NAME_LENGTH}'), ('distance', 'f8')]

        def calc_distance(arr):
            return np.array((arr[0], math.sqrt((arr[1].c_x - c_x)**2 + (arr[1].c_y - c_y)**2)), dtype=dtype)

        distances = np.apply_along_axis(calc_distance, 1, np.array(list(self.nodes.items())))
        return np.sort(distances, order='distance')[0][0]

    def _connect_current_point(self, entity, path):
        if 'pose' not in entity or 'point' not in entity['pose']['value']:
            return path

        c_x = entity['pose']['value']['point']['x']
        c_y = entity['pose']['value']['point']['y']
        x, y = self.potential.convert_pos(c_x, c_y)
        return [Node(x, y, c_x, c_y)] + path


class GridRedererMixin:
    BG_COLOR = (255, 255, 255)
    GRAPH_COLOR = (255, 51, 51)
    NODE_R = 2

    @classmethod
    def make_grid(cls, graph_size, nodes, edges):
        img = Image.new('RGB', graph_size, color=cls.BG_COLOR)
        draw = ImageDraw.Draw(img)
        for node in nodes.values():
            p = (node.x - cls.NODE_R, node.y - cls.NODE_R, node.x + cls.NODE_R, node.y + cls.NODE_R)
            draw.ellipse(p, fill=cls.GRAPH_COLOR)
        for edge in edges:
            draw.line((edge.st.as_tuple(), edge.ed.as_tuple()), fill=cls.GRAPH_COLOR)
        return img


class Potentials(MethodView, GridRedererMixin):
    NAME = 'potentials'

    def __init__(self, potential, graph_size, nodes, edges):
        super().__init__()
        self.potential = potential
        self.grid = GridRedererMixin.make_grid(graph_size, nodes, edges)

    def get(self, potential_id=None):
        logger.debug('Potentials.get')

        content_type = request.headers.get('Content-Type')
        accept = request.headers.get('Accept')

        if 'application/json' in (content_type, accept):
            if potential_id is None:
                return jsonify([{
                    'id': k,
                    'path': [str(n) for n in v['path']] if 'path' in v else []
                } for k, v in self.potential.potentials.items()])

            if potential_id in self.potential.potentials:
                v = self.potential.potentials[potential_id]
                return jsonify({
                    'id': potential_id,
                    'path': [str(n) for n in v['path']] if 'path' in v else []
                })

            abort(404, {
                'result': 'failure',
                'message': f'potential ({potential_id}) does not found',
            })

        output = io.BytesIO()
        potential_img = Image.fromarray(self.potential.get_current_field())
        Image.composite(self.grid, potential_img.convert('RGB'), potential_img).save(output, format='JPEG')

        response = make_response()
        response.data = output.getvalue()
        response.mimetype = 'image/jpeg'

        return response

    def delete(self, potential_id):
        logger.debug(f'Potentials.delete, potential_id={potential_id}')
        if not self.potential.has_potential(potential_id):
            abort(404, {
                'result': 'failure',
                'message': f'potential ({potential_id}) does not found',
            })

        self.potential.deregister(potential_id)
        return make_response('', 204)


class GraphViewer(MethodView, GridRedererMixin):
    NAME = 'graph_viewer'
    FONT_COLOR = (0, 0, 0)

    def __init__(self, graph_size, nodes, edges):
        super().__init__()
        self.enlarged_size = [e * const.GRAPH_MULTIPLY for e in graph_size]
        self.enlarged_nodes = {k: n.multiply(const.GRAPH_MULTIPLY) for k, n in nodes.items()}
        self.enlarged_edges = [Edge(e.st.multiply(const.GRAPH_MULTIPLY), e.ed.multiply(const.GRAPH_MULTIPLY)) for e in edges]

    def get(self):
        logger.debug('GraphVieer.get')

        output = io.BytesIO()
        grid = GridRedererMixin.make_grid(self.enlarged_size, self.enlarged_nodes, self.enlarged_edges)
        draw = ImageDraw.Draw(grid)
        for k, n in self.enlarged_nodes.items():
            draw.text((n.x + GridRedererMixin.NODE_R, n.y + GridRedererMixin.NODE_R), k, fill=GraphViewer.FONT_COLOR)
        grid.save(output, format='JPEG')

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
            msg = 'metadata_json does not exist'
            logger.warning(msg)
            return jsonify({
                'result': 'failure',
                'message': msg,
            }), 400
        metadata_json = request.files['metadata_json']

        u_length_m = float(request.form['u_length_m']) if 'u_length_m' in request.form else const.DEFAULT_UNIT_LENGTH

        grid = Grid(map_pgm, metadata_json, u_length_m)
        graph = grid.build_graph()

        nodes = {f'N{str(i).zfill(const.NODE_NAME_LENGTH - 1)}': Node(x=vertex.pixel[0],
                                                                      y=vertex.pixel[1],
                                                                      c_x=vertex.converted[0],
                                                                      c_y=vertex.converted[1])
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
