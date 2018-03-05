from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import Event
from cad.utils import log_cad


@api.route('/events/', methods=['GET'])
@json
def get_events():
    """
    Returns the URL of every event in the DB, both active and not active

    :return: ULRs of every events in the DB
    """
    return {'events': [event.get_url() for event in
                       Event.query.all()]}


@api.route('/events_raw/', methods=['GET'])
@json
def get_events_raw():
    """
    Returns the complete dataset of every event in the DB
    :return: The complete dataset of every event in the DB
    """
    return {'events_raw': [event.export_data() for event in
                           Event.query.all()]}


@api.route('/active_events/', methods=['GET'])
@json
def get_active_events():
    """
    Returns the URL of only active event in the DB

    :return: ULRs of only active events in the DB
    """
    return {'active_events': [event.get_url() for event in
                              Event.query.filter_by(active=True).all()]}


@api.route('/active_events_raw/', methods=['GET'])
@json
def get_active_events_raw():
    """
    Returns the complete dataset of only active event in the DB

    :return: The complete dataset of only active event in the DB
    """
    return {'active_events_raw': [event.export_data() for event in
                                  Event.query.filter_by(active=True).all()]}


@api.route('/events/<int:id>', methods=['GET'])
@json
def get_event(id):
    """
    Returns the complete dataset of the event given its ID
    :param id: The ID of the desired event
    :return: The complete dataset of the desired event
    """
    return Event.query.get_or_404(id).export_data()


@api.route('/events/', methods=['POST'])
@json
def new_event():
    event = Event()
    db.session.add(event)
    db.session.commit()

    log_cad(db,
            event_id=event.id,
            log_action='Event Created')

    if request.json:
        event = Event.query.get_or_404(event.id)
        event.import_data(request.json)
        db.session.add(event)
        db.session.commit()

    return {}, 201, {'Location': event.get_url()}


@api.route('/events/<int:id>', methods=['PUT'])
@json
def edit_event(id):
    event = Event.query.get_or_404(id)
    event.import_data(request.json)
    db.session.add(event)
    db.session.commit()

    return {}
