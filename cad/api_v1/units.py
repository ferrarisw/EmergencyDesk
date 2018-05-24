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
    db.session.add(unit)
    db.session.commit()

    log_cad(db=db,
            priority=1,
            log_action='Unit Created')

    if request.json:
        unit = Unit.query.get_or_404(unit.id)
        unit.import_data(request.json)
        db.session.add(unit)
        db.session.commit()

    return {}, 201, {'Location': unit.get_url()}


@api.route('/units/<unit_id>', methods=['PUT'])
@json
def edit_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    unit.import_data(request.json, log=True)
    db.session.add(unit)
    db.session.commit()

    return {}


@api.route('/units_live/<int:id>', methods=['PUT'])
@json
def edit_unit_live(id):
    """
    This API allows to edit unit data without taking track in the logs
    Use this, for example, for continuously edit the position of the unit from a client software

    :param id: The ID of the unit to edit
    :return: None
    """
    unit = Unit.query.get_or_404(id)
    unit.import_data(request.json, log=False)
    db.session.add(unit)
    db.session.commit()

    return {}
