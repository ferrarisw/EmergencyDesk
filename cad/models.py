import datetime

from flask import url_for, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    # TODO gestione password hash
    password = ''  # Questa variabile non viene mai settata, ma solo usata per permettere il cambio della pwd
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
        return {
            'id': self.id,
            'self_url': self.get_url(),
            'username': self.username,
            'password_hash': self.password_hash
        }

    def import_data(self, data):
        from cad.utils import generic_import_data
        return generic_import_data(self, data)


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
        return {
            'id': self.id,
            'self_url': self.get_url(),
            'active': self.active,
            'created': self.created,
            'created_by': self.created_by,
            'phone_number': self.phone_number,
            'country': self.country,
            'locality': self.locality,
            'adm_area_level_1': self.adm_area_level_1,
            'adm_area_level_2': self.adm_area_level_2,
            'adm_area_level_3': self.adm_area_level_3,
            'route': self.route,
            'street_number': self.street_number,
            'formatted_address': self.formatted_address,
            'lat': self.lat,
            'long': self.long,
            'status': self.status,
            'is_managed': self.is_managed,
            'is_managing': self.is_managing,
            'managing_user': self.managing_user,
            'emergency_place': self.emergency_place,
            'emergency_code': self.emergency_code,
            'emergency_criticity': self.emergency_criticity,
            'formatted_code': self.formatted_code,
            'unit_dispatched': self.unit_dispatched,
            'notes': self.notes
        }

    def import_data(self, data):
        from cad.utils import generic_import_data
        return generic_import_data(self, data)


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
