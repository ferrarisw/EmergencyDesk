import googlemaps
from flask import json
from flask.globals import _app_ctx_stack, _request_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable
from werkzeug.exceptions import NotFound
from werkzeug.urls import url_parse

from cad import db
from cad.exceptions import ValidationError
from cad.static import GMAPS_CONF


class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)


def set_field(instance: object, field: str, data) -> None:
    if data is False:
        super.__setattr__(instance, field, False)
    elif data is '' or not data:
        super.__setattr__(instance, field, None)
    else:
        super.__setattr__(instance, field, data)


def get_fields(instance: object):
    return [attr for attr in vars(instance)
            if not callable(getattr(instance, attr))
            and not attr.startswith("_")]


def log_cad(db: SQLAlchemy(),
            priority: int = 1,
            level: str = 'INFO',
            event_id: int = None,
            intervention_id: int = None,
            unit_id: int = None,
            log_action: str = None,
            log_message: str = None, ) -> None:
    from cad.models import Log
    log = Log(priority=priority,
              level=level,
              event_id=event_id,
              intervention_id=intervention_id,
              unit_id=unit_id,
              log_action=log_action,
              log_message=log_message)

    db.session.add(log)
    db.session.commit()


def generic_export_data(instance: object) -> dict:
    data = {}
    for attr in get_fields(instance):
        data[attr] = getattr(instance, attr)
    data['self_url'] = instance.get_url()
    return data


def split_url(url: str, method='GET'):
    """
    Returns the endpoint name and arguments that match a given URL. In
    other words, this is the reverse of Flask's url_for().
    """
    appctx = _app_ctx_stack.top
    reqctx = _request_ctx_stack.top
    if appctx is None:
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if reqctx is not None:
        url_adapter = reqctx.url_adapter
    else:
        url_adapter = appctx.url_adapter
        if url_adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed_url = url_parse(url)
    if parsed_url.netloc is not '' \
            and parsed_url.netloc != url_adapter.server_name:
        raise ValidationError('Invalid URL: ' + url)
    try:
        result = url_adapter.match(parsed_url.path, method)
    except NotFound:
        raise ValidationError('Invalid URL: ' + url)
    return result


def get_formatted_address(query: str) -> dict:
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    geocode_results = gm.geocode(query)[0]
    return geocode_results['formatted_address']


def get_lat_lng(query: str):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    geocode_results = gm.geocode(query)[0]

    lat = geocode_results["geometry"]["location"]["lat"]
    lng = geocode_results["geometry"]["location"]["lng"]

    return lat, lng


def get_compass_bearing(coords_1: tuple, coords_2: tuple) -> float:
    import math
    lat1 = math.radians(coords_1[0])
    lat2 = math.radians(coords_2[0])

    diffLong = math.radians(coords_2[1] - coords_1[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - \
        (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
