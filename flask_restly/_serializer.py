from flask import (
    Response,
    current_app,
)


def _serializer_factory(obj, callback, serializer):
    if serializer is None:
        serializer = current_app.config.get('RESTLY_DEFAULT_SERIALIZER')

    def wrapper(*args, **kwargs):
        response, code = callback(obj, *args, **kwargs)

        if isinstance(response, Response):
            return response, response.status_code

        return serializer(response) if response != '' else response, code

    return wrapper
