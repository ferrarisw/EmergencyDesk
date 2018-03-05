from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import InterventionEMS


@api.route('/interventions_ems/', methods=['GET'])
@json
def get_interventions_ems():
    """
    Returns the URL of every intervention_ems in the DB, both active and not active

    :return: ULRs of every interventions_ems in the DB
    """
    return {'interventions_ems': [intervention_ems.get_url() for intervention_ems in
                                  InterventionEMS.query.all()]}


@api.route('/interventions_ems_raw/', methods=['GET'])
@json
def get_interventions_ems_raw():
    """
    Returns the complete dataset of every intervention_ems in the DB

    :return: The complete dataset of every intervention_ems in the DB
    """
    return {'interventions_ems_raw': [intervention_ems.export_data() for intervention_ems in
                                      InterventionEMS.query.all()]}


@api.route('/active_interventions_ems/', methods=['GET'])
@json
def get_active_interventions_ems():
    """
    Returns the URL of only active intervention_ems in the DB

    :return: ULRs of only active interventions_ems in the DB
    """
    return {'active_interventions_ems': [intervention_ems.get_url() for intervention_ems in
                                         InterventionEMS.query.filter_by(active=True).all()]}


@api.route('/active_interventions_ems_raw/', methods=['GET'])
@json
def get_active_interventions_ems_raw():
    """
    Returns the complete dataset of only active intervention_ems in the DB

    :return: The complete dataset of only active intervention_ems in the DB
    """
    return {'active_interventions_ems_raw': [intervention_ems.export_data() for intervention_ems in
                                             InterventionEMS.query.filter_by(active=True).all()]}


@api.route('/interventions_ems/<int:id>', methods=['GET'])
@json
def get_intervention_ems(id):
    """
    Returns the complete dataset of the intervention_ems given its ID
    :param id: The ID of the desired intervention
    :return: The complete dataset of the desired intervention_ems
    """
    return InterventionEMS.query.get_or_404(id).export_data()


@api.route('/interventions_ems/<intervention_ems_id>', methods=['PUT'])
@json
def edit_intervention_ems(intervention_ems_id):
    intervention_ems = InterventionEMS.query.get_or_404(intervention_ems_id)
    intervention_ems.import_data(request.json)
    db.session.add(intervention_ems)
    db.session.commit()

    return {}


@api.route('/interventions_ems/<intervention_ems_id>/update_phase', methods=['PUT'])
@json
def edit_intervention_ems_phase(intervention_ems_id):
    intervention_ems = InterventionEMS.query.get_or_404(intervention_ems_id)
    intervention_ems.update_phase(request.json)
    db.session.add(intervention_ems)
    db.session.commit()

    return {}
