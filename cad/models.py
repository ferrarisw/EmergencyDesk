import datetime

from flask import url_for, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from cad.utils import get_fields, generic_export_data, set_field
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)

    def import_data(self, data):
        fields = get_fields(self)

        for field in fields:
            if data.get(field) is not None:

                '''Gestisce il cambiamento della password'''
                if field is 'password_hash' or 'password':
                    self.set_password(data[field])

                else:  # Caso generico
                    set_field(self, field, data[field])

        return self


class Event(db.Model):
    __tablename__ = 'events'

    # Basic Data

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    phone_number = db.Column(db.String(25), nullable=True)

    # Geolocation data

    country = db.Column(db.String(128), nullable=True)
    locality = db.Column(db.String(128), nullable=True)
    adm_area_level_1 = db.Column(db.String(128), nullable=True)
    adm_area_level_2 = db.Column(db.String(128), nullable=True)
    adm_area_level_3 = db.Column(db.String(128), nullable=True)
    route = db.Column(db.String(128), nullable=True)
    street_number = db.Column(db.String(128), nullable=True)
    formatted_address = db.Column(db.String(128), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)

    # Event Status

    status = db.Column(db.String(128), nullable=False, default='UNMANAGED')
    is_managed = db.Column(db.Boolean, nullable=False, default=False)
    is_managing = db.Column(db.Boolean, nullable=False, default=False)
    managing_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Event Data

    emergency_place = db.Column(db.String(1), nullable=True)
    emergency_code = db.Column(db.String(1), nullable=True)
    emergency_criticity = db.Column(db.String(1), nullable=True)
    formatted_code = db.Column(db.String(1), nullable=True)

    unit_dispatched = db.Column(db.Integer, default=0)
    notes = db.Column(db.String(255), nullable=True)

    def __init__(self):
        self.fields = [attr for attr in vars(self)
                       if not callable(getattr(self, attr))
                       and not attr.startswith("_")]

    def get_url(self):
        return url_for('api.get_event', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)

    def import_data(self, data):
        fields = get_fields(self)

        for field in fields:
            if data.get(field) is not None:

                '''
                Gestisce lo stato di attivita' dell'evento
                '''
                if field is 'active':
                    if data[field] == 'True':
                        set_field(self, 'active', True)
                    elif data[field] == 'False':
                        set_field(self, 'active', False)

                elif field is 'emergency_place' or 'emergency_code' or 'emergency_criticity':

                    old_place = getattr(self, 'emergency_place') or '*'
                    old_code = getattr(self, 'emergency_code') or '*'
                    old_criticity = getattr(self, 'emergency_criticity') or '*'

                    place = data.get('emergency_place') or '*'
                    code = data.get('emergency_code') or '*'
                    criticity = data.get('emergency_criticity') or '*'

                    formatted_code = (place or old_place) + (code or old_code) + (criticity or old_criticity)

                    # print('OLD ' + old_place + old_code + old_criticity)
                    # print('NEW ' + formatted_code)

                    set_field(self, field, data[field])
                    set_field(self, 'formatted_code', formatted_code)

                elif field is 'lat' or 'long':
                    set_field(self, field, float(data[field]))

                elif field is 'managing_user':
                    set_field(self, field, int(data[field]))

                elif field is 'id' or 'unit_dispatched' or 'created_by' or 'created':
                    # Questi campi non possono essere modificati manualmente
                    # ma sono settati automaticamente dal sistema
                    print("Non modificabile")
                    pass

                else:  # Caso generico
                    set_field(self, field, data[field])

        return self


class Mission(db.Model):
    __tablename__ = 'missions'

    # Basic Data

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    '''
    '''


class Unit(db.Model):
    __tablename__ = 'units'

    # Basic Data

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    '''
    '''


class Log(db.Model):
    __tablename__ = 'logs'

    # Basic Data

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    log = db.Column(db.String(255))
    '''
    '''