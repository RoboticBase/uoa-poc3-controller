import json

from flask import abort
import requests

from src import const


def get_entity(fiware_service, fiware_servicepath, entity_type, entity_id):
    if not (isinstance(fiware_service, str) and isinstance(fiware_servicepath, str)
            and isinstance(entity_type, str) and isinstance(entity_id, str)):
        raise TypeError('fiware_service, fiware_servicepath, entity_type and entity_id must be "str"')

    headers = __make_headers(fiware_service, fiware_servicepath)
    endpoint = f'{const.ORION_ENDPOINT}{const.ORION_BASE_PATH}{entity_id}'
    params = {
        'type': entity_type
    }
    result = requests.get(endpoint, headers=headers, params=params)
    if not (200 <= result.status_code < 300):
        code = result.status_code if result.status_code in (404, ) else 500
        abort(code, {
            'message': 'can not get an entity from orion',
            'root_cause': result.text if hasattr(result, 'text') else ''
        })
    try:
        result_json = result.json()
    except json.decoder.JSONDecodeError as e:
        abort(400, {
            'message': 'can not parse result',
            'root_cause': str(e)
        })
    return result_json


def __make_headers(fiware_service, fiware_servicepath, require_contenttype=False):
    headers = {
        'FIWARE-SERVICE': fiware_service,
        'FIWARE-SERVICEPATH': fiware_servicepath,
    }
    if require_contenttype:
        headers['Content-Type'] = 'application/json'

    return headers
