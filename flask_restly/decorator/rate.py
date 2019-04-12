from flask_restly._storage import push_metadata, get_metadata_storage
import wrapt


def limit(requests=None, window=None, group=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            return wrapped(*args, **kwargs)

        metadata = dict()

        if requests is not None:
            assert isinstance(requests, int), 'Requests amount must be a number'
            metadata['requests'] = requests

        if window is not None:
            assert isinstance(window, int), 'Window seconds must be a number'
            metadata['window'] = window

        if group is not None:
            assert isinstance(group, str), 'Group must be a string'
            metadata['group'] = group

        wrapped_func = wrapper(func)
        push_metadata(wrapped_func, dict(rating_limit=metadata))

        return wrapped_func

    return decorator


def resolver(func):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return wrapped(*args, **kwargs)

    wrapped_func = wrapper(func)
    get_metadata_storage().set('rate_limit_resolver', wrapped_func)

    return wrapped_func
