from flask import request

from cad import db
from cad.api_v1 import api
from cad.decorators import json
from cad.models import User


@api.route('/users/', methods=['GET'])
@json
def get_users():
    return {'users': [user.get_url() for user in User.query.all()]}


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
    return {}, 201, {'Location': user.get_url()}


@api.route('/users/<int:id>', methods=['PUT'])
@json
def edit_user(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return {}
