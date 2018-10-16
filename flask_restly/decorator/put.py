from flask_restly._storage import append_mapping
from functools import wraps


def put(path, serializer=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            length = len(response)

            assert length <= 2, 'Too much return items in PUT method'

            if length <= 1:
                return response, 201

            assert isinstance(response[1], int) is True, 'PUT response code should be a number'

            return response[0], response[1]

        append_mapping(wrapper, path, serializer, 'PUT')

        return wrapper

    return decorator
