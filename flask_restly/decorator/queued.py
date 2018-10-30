from flask_restly._storage import push_queued
from functools import wraps


def queued(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    push_queued(wrapper)

    return wrapper
