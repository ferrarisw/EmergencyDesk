from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import User, Log


@api.route('/users/', methods=['GET'])
@json
def get_users():
    return {'users': [user.get_url() for user in User.query.all()]}


@api.route('/users_raw/', methods=['GET'])
@json
def get_users_raw():
    return {'users_raw': [user.export_data() for user in
                          User.query.all()]}


@api.route('/users/<int:id>', methods=['GET'])
@json
def get_user(id):
    return User.query.get_or_404(id).export_data()


@api.route('/users/', methods=['POST'])
@json
def new_user():
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()

    log = Log(created_by='System', event_id=user.id, log_message='User Created')
    db.session.add(log)
    db.session.commit()

    return {}, 201, {'Location': user.get_url()}


@api.route('/users/<int:id>', methods=['PUT'])
@json
def edit_user(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()

    log = Log(created_by='System', log_action='User Data Modified')
    db.session.add(log)
    db.session.commit()

    return {}
