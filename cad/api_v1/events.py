from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import Event, Log


@api.route('/events/', methods=['GET'])
@json
def get_events():
    return {'events': [event.get_url() for event in
                       Event.query.all()]}


@api.route('/events_raw/', methods=['GET'])
@json
def get_events_raw():
    return {'events_raw': [event.export_data() for event in
                           Event.query.all()]}


@api.route('/active_events/', methods=['GET'])
@json
def get_active_events():
    return {'active_events': [event.get_url() for event in
                              Event.query.filter_by(active=True).all()]}


@api.route('/active_events_raw/', methods=['GET'])
@json
def get_active_events_raw():
    return {'active_events_raw': [event.export_data() for event in
                                  Event.query.filter_by(active=True).all()]}


@api.route('/events/<int:id>', methods=['GET'])
@json
def get_event(id):
    return Event.query.get_or_404(id).export_data()


@api.route('/events/', methods=['POST'])
@json
def new_event():
    event = Event()
    event.import_data(request.json)

    db.session.add(event)
    db.session.commit()

    log = Log(created_by='System', event_id=event.id, log_message='Event Created')
    db.session.add(log)
    db.session.commit()

    return {}, 201, {'Location': event.get_url()}


@api.route('/events/<int:id>', methods=['PUT'])
@json
def edit_event(id):
    event = Event.query.get_or_404(id)
    event.import_data(request.json)
    db.session.add(event)
    db.session.commit()

    log = Log(created_by='System', event_id=event.id, log_action='Event Data Modified')
    db.session.add(log)
    db.session.commit()

    return {}
