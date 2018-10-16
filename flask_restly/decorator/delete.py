from flask_restly._storage import append_mapping
from functools import wraps


def delete(path, queued=False, serializer=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return ('', 204) if result is None else (result, 200 if not queued else 202)

        append_mapping(wrapper, path, serializer, 'DELETE')

        return wrapper

    return decorator
