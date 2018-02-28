from cad.api_v1 import api
from cad.decorators import json
from .. import static


@api.route('/static/gmaps_conf/', methods=['GET'])
@json
def get_gmaps_conf():
    return static.GMAPS_CONF


@api.route('/static/event_ems_status/', methods=['GET'])
@json
def get_event_ems_status():
    return static.EVENT_EMS_STATUS


@api.route('/static/event_ems_place/', methods=['GET'])
@json
def get_event_ems_place():
    return static.EVENT_EMS_PLACE


@api.route('/static/event_ems_code/', methods=['GET'])
@json
def get_event_ems_code():
    return static.EVENT_EMS_CODE


@api.route('/static/event_ems_criticity/', methods=['GET'])
@json
def get_event_ems_criticity():
    return static.EVENT_EMS_CRITICITY


@api.route('/static/event_ems_type/', methods=['GET'])
@json
def get_event_ems_type():
    return static.EVENT_EMS_TYPE


@api.route('/static/unit_ems_status/', methods=['GET'])
@json
def get_unit_ems_status():
    return static.UNIT_EMS_STATUS


@api.route('/static/unit_ems_profile/', methods=['GET'])
@json
def get_unit_ems_profile():
    return static.UNIT_EMS_PROFILE


@api.route('/static/unit_ems_type/', methods=['GET'])
@json
def get_unit_ems_type():
    return static.UNIT_EMS_TYPE


@api.route('/static/intervention_ems_status/', methods=['GET'])
@json
def get_intervention_ems_status():
    return static.INTERVENTION_EMS_STATUS


@api.route('/static/intervention_ems_eval/', methods=['GET'])
@json
def get_intervention_ems_eval():
    return static.INTERVENTION_EMS_EVAL


@api.route('/static/intervention_ems_outcome/', methods=['GET'])
@json
def get_intervention_ems_outcome():
    return static.INTERVENTION_EMS_OUTCOME


@api.route('/static/logs_data/', methods=['GET'])
@json
def get_logs_data():
    return static.LOGS
