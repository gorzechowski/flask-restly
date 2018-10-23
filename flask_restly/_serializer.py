from flask import (
    Response,
    current_app,
)
from flask_restly._storage import get_metadata_storage


def _serializer_factory(instance, obj, callback, serializer):
    if serializer is None:
        serializer = current_app.config.get('RESTLY_DEFAULT_SERIALIZER')

    metadata = get_metadata_storage().get(obj.__name__).get(callback.__name__)
    outgoing = metadata.get('outgoing', None)

    def wrapper(*args, **kwargs):
        response, code = callback(instance, *args, **kwargs)

        if isinstance(response, Response):
            return response, response.status_code

        return serializer(response, outgoing) if response != '' else response, code

    return wrapper
