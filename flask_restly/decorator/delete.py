from flask_restly._storage import push_mapping
import wrapt


def delete(path, serialize=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            result = wrapped(*args, **kwargs)

            return ('', 204) if result is None else (result, 200)

        wrapped_func = wrapper(func)
        push_mapping(wrapped_func, path, serialize, 'DELETE')

        return wrapped_func

    return decorator
