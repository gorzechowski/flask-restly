from flask_restly._storage import append_mapping
from functools import wraps


def get(path, serialize=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            return response, 200

        append_mapping(wrapper, path, serialize, 'GET')

        return wrapper

    return decorator
