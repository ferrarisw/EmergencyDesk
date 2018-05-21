from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import InterventionEMS


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
