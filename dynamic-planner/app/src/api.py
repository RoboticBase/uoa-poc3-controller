import datetime
import io
import json

from logging import getLogger

from flask import jsonify, request, abort, make_response
from flask.views import MethodView

from PIL import Image

from src import const, orion
from src.fast_astar import FastAstar
from src.data import Mode, State

logger = getLogger(__name__)


class DynamicRoutePlanner(MethodView):
    NAME = 'dynamic_route_planner'

    def __init__(self, potential, graph_size, nodes, edges):
        super().__init__()
        self.potential = potential
        self.graph_size = graph_size
        self.nodes = nodes
        self.edges = edges

    def post(self):
        logger.debug('DynamicRoutePlanner.post')
        body = request.json

        if body is None or body.get('robotId') is None or body.get('startNode') is None or body.get('destNode') is None:
            abort(400, {
                'message': f'"robotId" and/or "startNode" and/or "destNode" do not exist, body={body}',
            })

        robot_id = body['robotId']
        start_node = body['startNode']
        dest_node = body['destNode']
        dest_angle = body.get('destAngle')

        entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id)
        if 'robotSize' not in entity or 'inflation_radius' not in entity['robotSize']['value']:
            return jsonify({
                'result': 'failure',
                'message': f'the "robotSize" of {robot_id} has not been initialized yet'
            }), 409

        infration_radius = float(entity['robotSize']['value']['inflation_radius'])
        radius = infration_radius/float(const.COSTMAP_METADATA['resolution'])

        fast_astar = FastAstar(
            self.nodes[start_node],
            self.nodes[dest_node],
            list(self.nodes.values()),
            self.graph_size,
            radius)
        searched_path = fast_astar.calculate(self.potential.current_field)
        self.potential.register(robot_id, searched_path, radius)

        payload = self._make_cmd(infration_radius, searched_path, dest_angle)

        result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id, payload)
        logger.info(f'send a "{const.START_COMMAND}" command to orion, '
                    f'result_status={result.status_code}, payload={json.dumps(payload)}')

        return jsonify({
            'result': 'success',
            'robotId': robot_id,
            'startNode': start_node,
            'destNode': dest_node,
            'destAngle': dest_angle,
            'orion_status': result.status_code,
        }), 201

    def _make_cmd(self, infration_radius, waypoints, dest_angle):
        t = datetime.datetime.now(const.TIMEZONE).isoformat(timespec='milliseconds')

        payload = {
            'naviCmd': {
                'type': 'command',
                'value': {
                    'time': t,
                    'command': const.START_COMMAND,
                    'metadata': {
                        'inflation_radius': infration_radius,
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
                r = data.get('robotSize', {}).get('value', {}).get('inflation_radius', const.DEFAULT_INFLATION_RADIUS)
                passed = self.potential.notify_pos(robot_id, c_x, c_y, r)
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
