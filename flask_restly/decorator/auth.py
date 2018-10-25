from functools import wraps
from flask_restly._storage import push_skip_authorization, get_metadata_storage


def unauthorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    push_skip_authorization(wrapper)

    return wrapper


def provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    get_metadata_storage().set('auth_provider', wrapper)

    return wrapper
