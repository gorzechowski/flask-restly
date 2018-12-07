from flask_restly._storage import push_metadata
import wrapt


def queued(func):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        return wrapped(*args, **kwargs)

    wrapped_func = wrapper(func)
    push_metadata(wrapped_func, {
        'queued': True,
    })

    return wrapped_func
