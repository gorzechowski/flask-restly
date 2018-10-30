from flask_restly._storage import push_metadata
from functools import wraps


def queued(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    push_metadata(wrapper, {
        'queued': True,
    })

    return wrapper
