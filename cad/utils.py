from flask.globals import _app_ctx_stack, _request_ctx_stack
from werkzeug.exceptions import NotFound
from werkzeug.urls import url_parse

from cad.exceptions import ValidationError
from cad.models import User


def get_attr(instance):
    return [attr for attr in vars(instance)
            if not callable(getattr(instance, attr))
            and not attr.startswith("_")]


def generic_import_data(instance, data):
    """
    Metodo generico di importazione dei dati.
    Da qui si gestiscono le richieste PUT eventualmente in base al tipo di dato
    richiesto.

    :param instance: oggetto sul quale eseguire la PUT
    :param data: parametri da impostare
    :return: oggetto con i dati modificati
    """
    fields = get_attr(instance)

    class_name = instance.__class__

    if class_name is User:
        user_import_data(instance, fields, data)
    else:
        for field in fields:
            if data.get(field) is not None:
                setattr(instance, field, data[field])

    return instance


def user_import_data(instance, fields, data):
    for field in fields:
        if data.get(field) is not None:
            if field is 'password_hash':  # Caso specifico per il cambio della password
                instance.set_password(data[field])
            else:  # Caso generico
                setattr(instance, field, data[field])


def split_url(url, method='GET'):
    """Returns the endpoint name and arguments that match a given URL. In
    other words, this is the reverse of Flask's url_for()."""
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
