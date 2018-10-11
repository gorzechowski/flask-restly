from flask import (
    current_app,
    Blueprint,
)
from flask_restly._storage import get_blueprints_storage, get_metadata_storage
from functools import wraps


def _wrapper_factory(obj, callback):
    def wrapper(*origin_args, **origin_kwargs):
        return callback(obj, *origin_args, **origin_kwargs)

    return wrapper


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

            if version not in blueprints.keys():
                bp = Blueprint(str(version), str(version), url_prefix='/api/rest/v%d/' % version)

                blueprints.set(version, bp)

            for value in metadata.get(obj.__name__, []):
                route = _build_route(name, value['path'], parent)

                blueprints.get(version).add_url_rule(
                    route,
                    value['func'].__name__,
                    _wrapper_factory(instance, value['func']),
                    methods=value['methods']
                )

            current_app.register_blueprint(blueprints.get(version))

            metadata.set(obj.__name__, list())

            return instance

        return wrapper

    return decorator
