from flask_restly._storage import push_metadata
import wrapt


def body(outgoing=None, incoming=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            return wrapped(*args, **kwargs)

        wrapped_func = wrapper(func)
        push_metadata(wrapped_func, {
            'incoming': incoming,
            'outgoing': outgoing,
        })

        return wrapped_func

    return decorator
