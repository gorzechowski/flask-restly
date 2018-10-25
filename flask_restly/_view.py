from flask import (
    Response,
    current_app,
    request,
)
from flask_restly._storage import get_metadata_storage
from flask_restly.exception import Forbidden


def _view_factory(instance, obj, callback, serialize):
    serializer = current_app.config.get('RESTLY_SERIALIZER')
    deserialize = serializer.deserialize

    if serialize is None:
        serialize = serializer.serialize

    metadata = get_metadata_storage().get(obj.__name__).get(callback.__name__)
    outgoing = metadata.get('outgoing', None)
    incoming = metadata.get('incoming', None)
    skip_auth = metadata.get('skip_authorization', False)

    def wrapper(*args, **kwargs):
        if not skip_auth and get_metadata_storage().get('auth_provider', lambda: True)() is False:
            raise Forbidden()

        if len(request.get_data()) > 0:
            kwargs['body'] = deserialize(request, incoming)

        response, code = callback(instance, *args, **kwargs)

        if isinstance(response, Response):
            return response, response.status_code

        return serialize(response, outgoing) if response != '' else response, code

    return wrapper
