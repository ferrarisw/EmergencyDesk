from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import Unit
from cad.utils import log_cad


@api.route('/units/', methods=['GET'])
@json
def get_units():
    return {'units': [unit.get_url() for unit in Unit.query.all()]}


@api.route('/units_raw/', methods=['GET'])
@json
def get_units_raw():
    return {'units_raw': [unit.export_data() for unit in
                          Unit.query.all()]}


@api.route('/units/<int:id>', methods=['GET'])
@json
def get_unit(id):
    return Unit.query.get_or_404(id).export_data()


@api.route('/units/', methods=['POST'])
@json
def new_unit():
    unit = Unit()
    unit.import_data(request.json)
    db.session.add(unit)
    db.session.commit()

    log_cad(db, created_by='System', log_action='Unit Created')

    return {}, 201, {'Location': unit.get_url()}


@api.route('/units/<int:id>', methods=['PUT'])
@json
def edit_unit(id):
    unit = Unit.query.get_or_404(id)
    unit.import_data(request.json)
    db.session.add(unit)
    db.session.commit()

    log_cad(db, created_by='System', log_action='Unit Data Modified')

    return {}
