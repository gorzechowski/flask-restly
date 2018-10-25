from flask_restly._storage import push_mapping
from functools import wraps


def patch(path, serialize=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            return ('', 204) if response is None else (response, 200)

        push_mapping(wrapper, path, serialize, 'PATCH')

        return wrapper

    return decorator
