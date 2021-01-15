import datetime
import json
import time

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

        if body is None or body.get('planId') is None or body.get('robotId') is None:
            msg = f'"planId" and/or "robotId" do not exist, body={body}'
            logger.warning(f'status=400, {msg}')
            abort(400, {
                'result': 'failure',
                'message': msg,
            })

        plan_id = body['planId']
        robot_id = body['robotId']
        payload = self._make_stop_cmd()
        result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id, payload)
        logger.info(f'send a "{const.STOP_COMMAND}" command to orion, '
                    f'result_status={result.status_code}, payload={json.dumps(payload)}')

        if const.COMMAND_RESULT_WAIT_ENABLE:
            for i in range(const.COMMAND_RESULT_WAIT_MAX_NUM):
                entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id)
                logger.warning(entity['naviCmd_status']['value'])
                if entity['naviCmd_status']['value'] == const.COMMAND_RESULT_OK:
                    break
                logger.debug(f'wait until naviCmd_status is OK, cnt={i}')
                time.sleep(const.COMMAND_RESULT_WAIT_SEC)
            else:
                return jsonify({
                    'result': 'failure',
                    'planId': plan_id,
                    'robotId': robot_id,
                    'reason': 'naviCmd_satus is still PENDING'
                }), 409
        else:
            time.sleep(const.COMMAND_RESULT_WAIT_SEC)

        plan = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.PLAN_TYPE, plan_id)
        payload = self._make_start_cmd(plan['waypoints']['value'])
        result = orion.send_command(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.ROBOT_TYPE, robot_id, payload)

        logger.info(f'send a "{const.START_COMMAND}" command to orion, '
                    f'result_status={result.status_code}, payload={json.dumps(payload)}')

        return jsonify({
            'result': 'success',
            'planId': plan_id,
            'robotId': robot_id,
            'orion_status': result.status_code,
        }), 201

    def _make_start_cmd(self, waypoints):
        if not isinstance(waypoints, list):
            msg = f'retrieved waypoints is not list, waypoints={waypoints}'
            logger.error(f'status=500, {msg}')
            abort(500, {
                'result': 'failure',
                'message': msg,
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

    def _make_stop_cmd(self):
        t = datetime.datetime.now(const.TIMEZONE).isoformat(timespec='milliseconds')

        payload = {
            'naviCmd': {
                'type': 'command',
                'value': {
                    'time': t,
                    'command': const.STOP_COMMAND,
                    'waypoints': []
                }
            }
        }
        return payload
