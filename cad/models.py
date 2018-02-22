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
            'self_url': self.get_url(),
            'username': self.username,
            'password': self.password_hash
        }

    def import_data(self, data):
        from cad.utils import generic_import_data
        return generic_import_data(self, data)

        '''
        fields = [attr for attr in vars(self)
                  if not callable(getattr(self, attr))
                  and not attr.startswith("_")]

        for field in fields:
            if data.get(field) is not None:
                setattr(self, field, data[field])

        return self
        '''


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    place = db.Column(db.String(128), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    active = db.Column(db.String(5), default='True')

    def __init__(self):
        self.fields = [attr for attr in vars(self)
                       if not callable(getattr(self, attr))
                       and not attr.startswith("_")]

    def get_url(self):
        return url_for('get_event', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'place': self.place,
            'created_by': self.created_by,
            'active': self.active
        }

    def import_data(self, data):
        from cad.utils import generic_import_data
        return generic_import_data(self, data)

        '''
        fields = [attr for attr in vars(self)
                  if not callable(getattr(self, attr))
                  and not attr.startswith("_")]

        for field in fields:
            if data.get(field) is not None:
                setattr(self, field, data[field])

        return self
        '''
