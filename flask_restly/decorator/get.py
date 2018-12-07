from flask_restly._storage import push_mapping
import wrapt


def get(path, serialize=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            response = wrapped(*args, **kwargs)

            return response, 200

        wrapped_func = wrapper(func)
        push_mapping(wrapped_func, path, serialize, 'GET')

        return wrapped_func

    return decorator
