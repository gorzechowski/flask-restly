from flask_restly._storage import push_metadata
from functools import wraps


def body(outgoing=None, incoming=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        push_metadata(wrapper, {
            'incoming': incoming,
            'outgoing': outgoing,
        })

        return wrapper

    return decorator
