from flask_restly._storage import push_metadata, get_metadata_storage
import wrapt


def unauthorized(func):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return wrapped(*args, **kwargs)

    wrapped_func = wrapper(func)
    push_metadata(wrapped_func, {
        'skip_authorization': True,
    })

    return wrapped_func


def provider(func):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return wrapped(*args, **kwargs)

    wrapped_func = wrapper(func)
    get_metadata_storage().set('auth_provider', wrapped_func)

    return wrapped_func
