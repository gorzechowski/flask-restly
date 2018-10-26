from flask_restly._storage import push_mapping
from functools import wraps


def get(path, serialize=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            return response, 200

        push_mapping(wrapper, path, serialize, 'GET')

        return wrapper

    return decorator
