from flask_restly._storage import push_mapping
import wrapt


def patch(path, serialize=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            response = wrapped(*args, **kwargs)

            return ('', 204) if response is None else (response, 200)

        wrapped_func = wrapper(func)
        push_mapping(wrapped_func, path, serialize, 'PATCH')

        return wrapped_func

    return decorator
