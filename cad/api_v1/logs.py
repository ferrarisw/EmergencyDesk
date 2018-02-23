from cad.api_v1 import api
from cad.decorators import json
from cad.models import Log


@api.route('/logs/', methods=['GET'])
@json
def get_logs():
    return {'logs': [log.get_url() for log in Log.query.all()]}


@api.route('/logs_raw/', methods=['GET'])
@json
def get_logs_raw():
    return {'logs_raw': [log.export_data() for log in
                         Log.query.all()]}


@api.route('/logs/<int:event_id>', methods=['GET'])
@json
def get_logs_event(event_id):
    return {'logs_event': [log.export_data() for log in
                           Log.query.filter_by(event_id=event_id).all()]}
