from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import Event, InterventionEMS, Log
from cad.utils import log_cad


@api.route('/events_raw/', methods=['GET'])
@json
def get_events_raw():
    """
    Returns the complete dataset of every event in the DB
    :return: The complete dataset of every event in the DB
    """
    return {'events_raw': [event.export_data_raw() for event in
                           Event.query.all()]}


@api.route('/active_events_raw/', methods=['GET'])
@json
def get_active_events_raw():
    """
    Returns the complete dataset of only active event in the DB

    :return: The complete dataset of only active event in the DB
    """
    return {'active_events_raw': [event.export_data_raw() for event in
                                  Event.query.filter_by(active=True).all()]}


@api.route('/events/', methods=['POST'])
@json
def new_event():
    event = Event()
    db.session.add(event)
    db.session.commit()

    log_cad(db,
            event_id=event.id,
            log_action='event_created')

    if request.json:
        event = Event.query.get_or_404(event.id)
        event.import_data(request.json)
        db.session.add(event)
        db.session.commit()

    return {}, 201, {'Location': event.get_url()}


@api.route('/events/<int:event_id>/create_interventions_ems', methods=['POST'])
@json
def new_intervention_ems(event_id):
    event = Event.query.get_or_404(event_id)
    intervention_ems = InterventionEMS(event_id=event_id, unit_progressive=event.unit_dispatched + 1)

    db.session.add(intervention_ems)
    db.session.commit()

    log_cad(db,
            priority=1,
            event_id=event.id,
            intervention_id=intervention_ems.id,
            log_action='intervention_ems_created',
            log_message='InterventionEMS ' + str(intervention_ems.id) + ' Created for Event ' + str(event_id))

    event.unit_dispatched += 1
    event.interventions_ems.append(intervention_ems)
    db.session.add(event)
    db.session.commit()

    if request.json:
        intervention_ems.import_data(request.json)
        db.session.add(intervention_ems)
        db.session.commit()

    return {}, 201, {'Location': event.get_url()}


@api.route('/events/<event_id>/logs_raw', methods=['GET'])
@json
def get_logs_raw_by_event_id(event_id):
    return {'logs_raw': [logs.export_data() for logs in
                         Log.query.filter_by(event_id=event_id).all()]}


@api.route('/events/<int:id>', methods=['PUT'])
@json
def edit_event(id):
    event = Event.query.get_or_404(id)
    event.import_data(request.json)
    db.session.add(event)
    db.session.commit()

    return {}
