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
        entity = orion.get_entity(const.FIWARE_SERVICE, const.FIWARE_SERVICEPATH, const.PLAN_TYPE, plan_id)

        logger.debug(entity)

        return jsonify({
            'result': 'success',
            'planId': plan_id,
        }), 201
