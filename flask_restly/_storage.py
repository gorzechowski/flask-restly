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


def append_mapping(func, path, serializer, method):
    parent_name = _get_func_parent_name(func)
    metadata = get_metadata_storage()

    if not any(parent_name == key for key in metadata.keys()):
        metadata.set(parent_name, {
            func.__name__: {},
        })

    metadata.get(parent_name).get(func.__name__, {}).update(
        {
            'func': func,
            'path': path,
            'serializer': serializer,
            'methods': [method],
        }
    )


def append_body_types(func, incoming, outgoing):
    parent_name = _get_func_parent_name(func)
    metadata = get_metadata_storage()

    if not any(parent_name == key for key in metadata.keys()):
        metadata.set(parent_name, {
            func.__name__: {},
        })

    metadata.get(parent_name).get(func.__name__, {}).update(
        {
            'incoming': incoming,
            'outgoing': outgoing,
        }
    )


def _get_func_parent_name(func):
    parts = func.__qualname__.split('.')
    return parts[len(parts) - 2]
