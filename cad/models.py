import datetime

from flask import url_for, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from cad.utils import get_fields, generic_export_data, set_field, JsonEncodedDict, log_cad
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

        updated = False

        for field in fields:
            if data.get(field) is not None:

                updated = True

                if field is 'password_hash' or 'password':
                    self.set_password(data[field])

                else:  # Caso generico
                    set_field(self, field, data[field])

        if updated:
            log_cad(db=db,
                    log_action='User Data Modified',
                    log_message=str(data))

        return self


class Event(db.Model):
    __tablename__ = 'events'

    # Basic Data

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    updated = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    closed = db.Column(db.DateTime, nullable=True)
    closed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Geolocation data

    phone_number = db.Column(db.String(25), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    locality = db.Column(db.String(128), nullable=True)
    adm_area_level_1 = db.Column(db.String(128), nullable=True)
    adm_area_level_2 = db.Column(db.String(128), nullable=True)
    adm_area_level_3 = db.Column(db.String(128), nullable=True)
    route = db.Column(db.String(128), nullable=True)
    street_number = db.Column(db.String(128), nullable=True)
    formatted_address = db.Column(db.String(128), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    geolocation_data = db.Column(JsonEncodedDict, nullable=True)

    # Event Status

    status = db.Column(db.String(128), nullable=False, default='UNMANAGED')
    is_editing = db.Column(db.Boolean, nullable=False, default=False)
    is_managed = db.Column(db.Boolean, nullable=False, default=False)
    is_managing = db.Column(db.Boolean, nullable=False, default=False)
    managing_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    dispatch_delayed = db.Column(db.DateTime, nullable=True)
    dispatch_date = db.Column(db.DateTime, nullable=True)

    # Event Data

    type = db.Column(db.String(10), nullable=True)
    place = db.Column(db.String(1), nullable=True)
    code = db.Column(db.String(3), nullable=True)
    criticity = db.Column(db.String(1), nullable=True)
    formatted_code = db.Column(db.String(5), nullable=True)

    interventions_ems = db.relationship('InterventionEMS', backref='event')
    unit_dispatched = db.Column(db.Integer, default=0)
    notes = db.Column(db.String(255), nullable=True)

    def get_url(self):
        return url_for('api.get_event', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)

    def import_data(self, data):
        fields = get_fields(self)

        updated = False

        for field in fields:
            if data.get(field) is not None:

                if field is 'active':
                    if data[field] == 'True':
                        set_field(self, 'active', True)
                    elif data[field] == 'False':
                        set_field(self, 'active', False)
                    updated = True

                elif field is 'place' or 'code' or 'criticity':

                    old_place = getattr(self, 'place') or '*'
                    old_code = getattr(self, 'code') or '*'
                    old_criticity = getattr(self, 'criticity') or '*'

                    place = data.get('place') or '*'
                    code = data.get('code') or '*'
                    criticity = data.get('criticity') or '*'

                    formatted_code = (place or old_place) + (code or old_code) + (criticity or old_criticity)

                    set_field(self, field, data[field])
                    set_field(self, 'formatted_code', formatted_code)
                    updated = True

                elif field is 'lat' or 'lng':
                    set_field(self, field, float(data[field]))
                    updated = True

                elif field is 'managing_user':
                    set_field(self, field, int(data[field]))
                    updated = True

                elif field is 'geolocation_data':
                    set_field(self, field, int(data[field]))
                    updated = True

                elif field is 'id' or 'unit_dispatched' or 'created_by' or 'created':
                    # Questi campi non possono essere modificati manualmente
                    # ma sono settati automaticamente dal sistema
                    print("Non modificabile")
                    pass

                else:  # Caso generico
                    set_field(self, field, data[field])
                    updated = True

        if updated:
            self.updated = datetime.datetime.now()
            log_cad(db=db,
                    event_id=self.id,
                    log_action='Event Data Modified',
                    log_message=str(data))

        return self


class InterventionEMS(db.Model):
    __tablename__ = 'interventions_ems'

    # Basic Data
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, default=datetime.datetime.now())
    updated = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    closed = db.Column(db.DateTime, nullable=True)

    active = db.Column(db.Boolean, nullable=False, default=True)
    status = db.Column(db.String(32), nullable=False, default='CREATED')
    is_editing = db.Column(db.Boolean, nullable=False, default=False)
    is_managed = db.Column(db.Boolean, nullable=False, default=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)

    unit_call_sign = db.Column(db.String(64), db.ForeignKey('units.call_sign'))
    unit_profile = db.Column(db.String(64))
    unit_type = db.Column(db.String(64))
    unit_progressive = db.Column(db.Integer)

    alarmed = db.Column(db.Boolean, nullable=True, default=False)
    blu_event = db.Column(db.Boolean, nullable=True)
    formatted_address = db.Column(db.String(128), nullable=True)

    date_IN = db.Column(db.DateTime)
    date_PA = db.Column(db.DateTime)
    date_AR = db.Column(db.DateTime)
    date_CA = db.Column(db.DateTime)
    date_FIN = db.Column(db.DateTime)

    outcome = db.Column(db.String(128), nullable=True)
    sanitary_eval = db.Column(db.String(1), nullable=True)
    destination = db.Column(db.String(128), nullable=True)

    def get_url(self):
        return url_for('api.get_intervention_ems', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)

    def import_data(self, data):
        fields = get_fields(self)

        updated = False

        for field in fields:
            if data.get(field) is not None:

                if field in ['alarmed', 'blu_event', 'is_editing', 'is_managed']:
                    if data[field] == 'True':
                        set_field(self, field, True)
                    elif data[field] == 'False':
                        set_field(self, field, False)
                    updated = True
                    continue

                elif field in ['active']:
                    if data[field] == 'True':
                        set_field(self, field, True)

                    elif data[field] == 'False':
                        set_field(self, 'closed', datetime.datetime.now())
                        set_field(self, 'active', False)
                    updated = True
                    continue

                elif field in ['date_IN', 'date_PA', 'date_AR', 'date_CA', 'date_FIN']:
                    from dateutil import parser
                    set_field(self, field, parser.parse(data[field]))
                    updated = True
                    continue

                elif field in ['id', 'event_id', 'unit_id', 'unit_progressive']:
                    log_cad(db=db,
                            priority=5,
                            mode='WARN',
                            event_id=self.event_id,
                            intervention_ems_id=self.id,
                            unit_id=self.unit_id,
                            log_action='Try to edit non editable data',
                            log_message="{'" + field + "': '" + data[field] + "'}")
                    continue

                else:
                    set_field(self, field, data[field])
                    updated = True

        if updated:
            self.updated = datetime.datetime.now()
            log_cad(db=db,
                    event_id=self.event_id,
                    intervention_ems_id=self.id,
                    unit_id=self.unit_id,
                    log_action='InterventionEMS Data Modified',
                    log_message=str(data))

        return self

    def update_phase(self, data):
        if data.get('phase') is not None and data.get('phase') in ['IN', 'PA', 'AR', 'CA', 'FIN']:
            set_field(self, field='date_' + data.get('phase'), data=datetime.datetime.now())
            self.updated = datetime.datetime.now()
            log_cad(db=db,
                    priority=2,
                    event_id=self.event_id,
                    intervention_ems_id=self.id,
                    log_action='InterventionEMS Phase Modified',
                    log_message="{" + "'date_" + data.get('phase') + ": '" + str(datetime.datetime.now()) + "'}")


class Unit(db.Model):
    __tablename__ = 'units'

    # Basic Data

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default='OPERATIVE')
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    call_sign = db.Column(db.String(64))
    profile = db.Column(db.String(64))
    type = db.Column(db.String(64))

    current_address = db.Column(db.String(128), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    event_dispatched = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    intervention_dispatched = db.Column(db.Integer, db.ForeignKey('interventions_ems.id'), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def get_url(self):
        return url_for('api.get_unit', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)

    def import_data(self, data, log=False):
        fields = get_fields(self)

        updated = False
        update_address = update_lat_lng = False

        for field in fields:
            if data.get(field) is not None:
                updated = True
                if field in ['lat', 'lng']:
                    update_address = True
                    continue

                elif field in ['current_address']:
                    if data.get(field) is '':
                        set_field(self, 'lat', None)
                        set_field(self, 'lng', None)
                        set_field(self, 'current_address', None)
                    else:
                        set_field(self, 'current_address', data[field])
                        update_lat_lng = True

                    continue

                elif field in ['active']:
                    if data[field] is 'True':
                        set_field(self, field, True)
                    elif data[field] is 'False':
                        set_field(self, field, False)
                    continue

                else:
                    set_field(self, field, data[field])

        if update_address:
            from cad.utils import get_formatted_address
            set_field(self, 'current_address', get_formatted_address('{} {}'.format(self.lat, self.lng)))

        if update_lat_lng:
            from cad.utils import get_lat_lng, get_formatted_address
            lat, lng = get_lat_lng(self.current_address)
            set_field(self, 'current_address', get_formatted_address(self.current_address))
            set_field(self, 'lat', lat)
            set_field(self, 'lng', lng)

        if updated and not log:
            log_cad(db=db,
                    priority=1,
                    intervention_ems_id=self.intervention_dispatched,
                    event_id=self.event_dispatched,
                    log_action='Unit Data Modified',
                    log_message=str(data))

        return self


class Log(db.Model):
    __tablename__ = 'logs'

    # Basic Data

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, default=1)
    level = db.Column(db.String(5), nullable=False, default='INFO')

    created = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    intervention_ems_id = db.Column(db.Integer, db.ForeignKey('interventions_ems.id'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)

    log_action = db.Column(db.String(128), nullable=False, default='')
    log_message = db.Column(db.Text, nullable=True)

    def get_url(self):
        return url_for('api.get_logs', id=self.id, _external=True)

    def export_data(self):
        return generic_export_data(self)
