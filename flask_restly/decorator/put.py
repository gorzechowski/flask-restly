from flask_restly._storage import push_mapping
import wrapt


def put(path, serialize=None):
    def decorator(func):
        @wrapt.decorator
        def wrapper(wrapped, _, args, kwargs):
            response = wrapped(*args, **kwargs)
            length = len(response)

            assert length <= 2, 'Too much return items in PUT method'

            if length <= 1:
                return response, 201

            assert isinstance(response[1], int) is True, 'PUT response code should be a number'

            return response[0], response[1]

        wrapped_func = wrapper(func)
        push_mapping(wrapped_func, path, serialize, 'PUT')

        return wrapped_func

    return decorator
