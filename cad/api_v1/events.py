from flask import jsonify, request

from cad import db
from cad.api_v1 import api
from cad.models import Event


@api.route('/events/', methods=['GET'])
def get_events():
    return jsonify({'events': [event.get_url() for event in
                               Event.query.all()]})


@api.route('/active_events/', methods=['GET'])
def get_active_events():
    return jsonify({'active_events': [event.get_url() for event in
                                      Event.query.filter_by(active=True).all()]})


@api.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    return jsonify(Event.query.get_or_404(id).export_data())


@api.route('/events/', methods=['POST'])
def new_events():
    events = Event()
    events.import_data(request.json)
    db.session.add(events)
    db.session.commit()
    return jsonify({}), 201, {'Location': events.get_url()}


@api.route('/events/<int:id>', methods=['PUT'])
def edit_events(id):
    events = Event.query.get_or_404(id)
    events.import_data(request.json)
    db.session.add(events)
    db.session.commit()
    return jsonify({})
