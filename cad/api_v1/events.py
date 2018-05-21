import http

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


@api.route('/events/<int:id>/lock', methods=['GET'])
@json
def lock_event(id):
    """
    This method allows you to block write access to an event by setting the is_managing parameter to True. The aim is to
    avoid data consistency problems due to the high level of competition to which this system may be subject.

    To block an event you must provide the username of the person who requests it. If this is not provided, the request
    will be rejected with status code 417 (EXPECTATION_FAILED).

    It is then verified that the event was not already blocked by another user. If yes, the request is rejected with
    status code 423 (UNAUTHORIZED).

    If the procedure passes these checks positively, then the event status is changed by setting is_managing = True and
    managing_user with the username of the person who requested it.

    :param id: The event ID to be unlocked
    :return: The HTTP Status Code of the lock request
    """
    json_data = request.json

    # When necessary data are not provided (managing_user) 417
    if not json_data['managing_user']:
        return {'message': 'Missing information managing_user',
                'status': http.HTTPStatus.EXPECTATION_FAILED}, http.HTTPStatus.EXPECTATION_FAILED

    event = Event.query.get_or_404(id)

    # When the resource is already locked - 423
    if event.is_managing:
        return {'message': 'Event already locked',
                'status': http.HTTPStatus.UNAUTHORIZED}, http.HTTPStatus.UNAUTHORIZED

    locking_data = {
        'is_managing': True,
        'managing_user': json_data['managing_user'],
        'updated_by': json_data['managing_user']
    }

    event.import_data(locking_data)
    db.session.add(event)
    db.session.commit()

    return {'message': 'Event correctly locked',
            'status': http.HTTPStatus.OK}, http.HTTPStatus.OK


@api.route('/events/<int:id>/unlock', methods=['GET'])
@json
def unlock_event(id):
    """
    This method allows you to unlock an event from a previously taken lock. This will allow other users to write access
    event data.

    To unlock an event, you must provide the user name of the event requester. If this is not provided, the request will
    be rejected with status code 417 (EXPECTATION_FAILED).

    It is then verified that the event was blocked by the supplied user. Otherwise, the request will be rejected with a
    status code 423 (UNAUTHORIZED).

    If the procedure passes these checks positively, then the event status is changed by setting is_managing = False and
    emptying the managing_user parameter.

    :param id: The event ID to be unlocked
    :return: The HTTP Status Code of the unlock request
    """
    json_data = request.json

    # When necessary data are not provided (managing_user)
    if not json_data['managing_user']:
        return {'message': 'Missing information managing_user',
                'status': http.HTTPStatus.EXPECTATION_FAILED}, http.HTTPStatus.EXPECTATION_FAILED

    event = Event.query.get_or_404(id)

    # When the resource is already unlocked
    if not event.is_managing:
        return {'message': 'Event already unlocked',
                'status': http.HTTPStatus.UNAUTHORIZED}, http.HTTPStatus.UNAUTHORIZED

    # TODO Verify admin permissions with a query and not json_data
    if event.is_managing and event.managing_user is not json_data['managing_user'] and not json_data['is_admin']:
        return {'message': 'User is not allowed to unlock this event',
                'status': http.HTTPStatus.UNAUTHORIZED}, http.HTTPStatus.UNAUTHORIZED

    locking_data = {
        'is_managing': False,
        'managing_user': None,
        'updated_by': json_data['managing_user']
    }

    event.import_data(locking_data)
    db.session.add(event)
    db.session.commit()

    return {'message': 'Event correctly unlocked',
            'status': http.HTTPStatus.OK}, http.HTTPStatus.OK
