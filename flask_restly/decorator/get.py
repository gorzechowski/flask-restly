from flask_restly._storage import append_mapping
from functools import wraps
from flask import jsonify


def get(path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return jsonify(func(*args, **kwargs))

        append_mapping(wrapper, path, 'GET')

        return wrapper

    return decorator
