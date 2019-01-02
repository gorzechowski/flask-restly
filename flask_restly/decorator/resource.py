from flask import (
    current_app,
    Blueprint,
)
from flask_restly._storage import get_blueprints_storage, get_metadata_storage
from flask_restly._view import _view_factory
from flask_restly._url_rule import _build_rule_name, _build_route
from functools import wraps


def resource(name, parent=None, version=1):
    assert type(name) is str, 'Resource name should be a string'
    assert len(name) > 0, 'Resource name should contain at least one char'

    def decorator(obj):
        obj._resource_name = name
        obj._parent = parent if parent is not None else None

        @wraps(obj)
        def wrapper(*args, **kwargs):
            instance = obj(*args, **kwargs)

            metadata = get_metadata_storage()
            blueprints = get_blueprints_storage()
            api_prefix = current_app.config.get('RESTLY_API_PREFIX').strip('/')

            if version not in blueprints.keys():
                bp = Blueprint('v%d' % version, __name__, url_prefix='/%s/v%d/' % (api_prefix, version))

                blueprints.set(version, bp)

            for key, value in metadata.get(obj.__name__, {}).items():
                route = _build_route(obj, value['path'])
                rule_name = _build_rule_name(obj, value['func'].__name__)
                view = _view_factory(instance, obj, value['func'], value['serialize'])

                blueprints.get(version).add_url_rule(
                    route,
                    rule_name,
                    view,
                    methods=[value['method']],
                )

            current_app.register_blueprint(blueprints.get(version))

            return instance

        return wrapper

    return decorator
