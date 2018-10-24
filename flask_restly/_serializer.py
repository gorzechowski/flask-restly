from flask import (
    Response,
    current_app,
    request,
)
from flask_restly._storage import get_metadata_storage


def _serializer_factory(instance, obj, callback, serializer):
    if serializer is None:
        serializer = current_app.config.get('RESTLY_DEFAULT_SERIALIZER').serialize
        deserializer = current_app.config.get('RESTLY_DEFAULT_SERIALIZER').deserialize

    metadata = get_metadata_storage().get(obj.__name__).get(callback.__name__)
    outgoing = metadata.get('outgoing', None)
    incoming = metadata.get('incoming', None)

    def wrapper(*args, **kwargs):
        if len(request.get_data()) > 0:
            kwargs['body'] = deserializer(request, incoming)

        response, code = callback(instance, *args, **kwargs)

        if isinstance(response, Response):
            return response, response.status_code

        return serializer(response, outgoing) if response != '' else response, code

    return wrapper
