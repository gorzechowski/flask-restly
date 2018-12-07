from flask_restly._storage import get_metadata_storage
import wrapt


def provider(func):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return wrapped(*args, **kwargs)

    wrapped_func = wrapper(func)
    get_metadata_storage().set('identity_provider', wrapped_func)

    return wrapped_func
