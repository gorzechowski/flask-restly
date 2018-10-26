from flask_restly._storage import push_body_types
from functools import wraps


def body(outgoing=None, incoming=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        push_body_types(wrapper, incoming, outgoing)

        return wrapper

    return decorator
