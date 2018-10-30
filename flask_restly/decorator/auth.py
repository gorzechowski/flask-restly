from functools import wraps
from flask_restly._storage import push_metadata, get_metadata_storage


def unauthorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    push_metadata(wrapper, {
        'skip_authorization': True,
    })

    return wrapper


def provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    get_metadata_storage().set('auth_provider', wrapper)

    return wrapper
