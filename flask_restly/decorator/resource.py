from flask import (
    current_app,
    Blueprint,
)
from flask_restly._storage import get_blueprints_storage, get_metadata_storage
from flask_restly._serializer import _serializer_factory
from functools import wraps


def _build_route(name, path, parent):
    route = ''

    if parent is not None:
        if hasattr(parent, '_parent_name'):
            route += parent._parent_name + '/<%s_id>/' % parent._parent_name

        route += parent._resource_name + '/<%s_id>/' % parent._resource_name

    route += name + path.rstrip('/')

    return route


def resource(name, parent=None, version=1):
    assert name is not None, 'Resource name can not be empty'

    def decorator(obj):
        obj._resource_name = name

        if parent is not None:
            obj._parent_name = parent._resource_name

        @wraps(obj)
        def wrapper(*args, **kwargs):
            instance = obj(*args, **kwargs)

            metadata = get_metadata_storage()
            blueprints = get_blueprints_storage()
            api_prefix = current_app.config.get('RESTLY_API_PREFIX').strip('/')

            if version not in blueprints.keys():
                bp = Blueprint(str(version), str(version), url_prefix='/%s/v%d/' % (api_prefix, version))

                blueprints.set(version, bp)

            for key, value in metadata.get(obj.__name__, {}).items():
                route = _build_route(name, value['path'], parent)

                blueprints.get(version).add_url_rule(
                    route,
                    value['func'].__name__,
                    _serializer_factory(instance, obj, value['func'], value['serialize']),
                    methods=value['methods']
                )

            current_app.register_blueprint(blueprints.get(version))

            metadata.set(obj.__name__, {
                obj.__name__: {},
            })

            return instance

        return wrapper

    return decorator
