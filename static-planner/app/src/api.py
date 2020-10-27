import datetime
import json

from logging import getLogger

from flask import jsonify, request, abort
from flask.views import MethodView

from src import const, orion

logger = getLogger(__name__)


class StaticRoutePlanner(MethodView):
    NAME = 'static_route_planner'

    def post(self):
        logger.debug('StaticRoutePlanner.post')
        body = request.json

        if body is None or body.get('planId') is None:
            abort(400, {
                'message': f'"planId" does not found, body={body}',
            })

        plan_id = body['planId']
        robot_id = body['robotId']
        entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.PLAN_TYPE, plan_id)
        payload = self._make_cmd(entity['waypoints']['value'])
        result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id, payload)
        logger.info(f'send a "{const.START_COMMAND}" command to orion, '
                    f'result_status={result.status_code}, payload={json.dumps(payload)}')

        return jsonify({
            'result': 'success',
            'planId': plan_id,
            'orion_status': result.status_code,
        }), 201

    def _make_cmd(self, waypoints):
        if not isinstance(waypoints, list):
            abort(500, {
                'message': f'retrieved waypoints is not list, waypoints={waypoints}'
            })
        t = datetime.datetime.now(const.TIMEZONE).isoformat(timespec='milliseconds')

        payload = {
            'naviCmd': {
                'type': 'command',
                'value': {
                    'time': t,
                    'command': const.START_COMMAND,
                    'waypoints': waypoints,
                }
            }
        }
        return payload
