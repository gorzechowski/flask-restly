import inspect


class KeyValueStorage:
    _storage = {}

    def set(self, key, value):
        self._storage[key] = value

    def get(self, key, default_value=None):
        return self._storage.get(key, default_value)

    def keys(self):
        return self._storage.keys()

    def clear(self):
        self._storage = {}


_metadata = KeyValueStorage()
_blueprints = KeyValueStorage()


def get_metadata_storage():
    return _metadata


def get_blueprints_storage():
    return _blueprints


def push_mapping(func, path, serialize, method):
    parent_name = _get_func_parent_name(func)
    metadata = get_metadata_storage()

    if _has_arg_declared(func, 'identity'):
        push_metadata(func, {
            'inject_identity': True,
        })

    if _has_arg_declared(func, 'body'):
        push_metadata(func, {
            'inject_body': True,
        })

    if not any(parent_name == key for key in metadata.keys()):
        metadata.set(parent_name, {
            func.__name__: {},
        })

    data = metadata.get(parent_name).get(func.__name__, {}).copy()

    data.update(
        {
            'func': func,
            'path': path,
            'serialize': serialize,
            'method': method,
        }
    )

    metadata.get(parent_name)[func.__name__] = data


def push_metadata(func, new_data):
    parent_name = _get_func_parent_name(func)
    metadata = get_metadata_storage()

    if not any(parent_name == key for key in metadata.keys()):
        metadata.set(parent_name, {
            func.__name__: {},
        })

    data = metadata.get(parent_name).get(func.__name__, {}).copy()

    data.update(new_data)

    metadata.get(parent_name)[func.__name__] = data


def _get_func_parent_name(func):
    parts = func.__qualname__.split('.')
    return parts[len(parts) - 2]


def _has_arg_declared(func, arg_name):
    inspection = inspect.getfullargspec(func)

    return any(arg == arg_name for arg in inspection.args)
