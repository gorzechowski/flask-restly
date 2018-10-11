from flask_restly._storage import append_mapping
from functools import wraps
from flask import jsonify


def put(path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            length = len(response)

            assert length <= 2, 'Too much return items in PUT method'

            if length <= 1:
                return jsonify(response), 201

            assert isinstance(response[1], int) is True, 'PUT response code should be a number'

            return jsonify(response[0]), response[1]

        append_mapping(wrapper, path, 'PUT')

        return wrapper

    return decorator
