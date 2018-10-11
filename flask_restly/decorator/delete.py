from flask_restly._storage import append_mapping
from functools import wraps
from flask import jsonify


def delete(path, **dec_kwargs):
    def decorator(func):
        queued = dec_kwargs.get('queued', False)

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return ('', 204) if result is None else (jsonify(result), 200 if not queued else 202)

        append_mapping(wrapper, path, 'DELETE')

        return wrapper

    return decorator
