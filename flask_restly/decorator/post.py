from flask_restly._storage import append_mapping
from functools import wraps
from flask import jsonify


def post(path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return ('', 204) if result is None else (jsonify(result), 200)

        append_mapping(wrapper, path, 'POST')

        return wrapper

    return decorator
