from flask import request, jsonify, Flask, current_app
from werkzeug.exceptions import HTTPException
from flask_restly.exception import InternalServerError
from flask_restly.serializer import json
from ._storage import get_blueprints_storage, get_metadata_storage
from ._rate import inject_rate_limit_headers


__version__ = '1.1.0'


def _jsonify_error(error):
    return jsonify(dict(error=error.description))


def api_error_handler(error):
    """
    :param error:
    :type error:  HTTPException
    :return:
    """
    if not request.path.startswith(current_app.config.get('RESTLY_API_PREFIX')):
        raise error

    if isinstance(error, HTTPException):
        return _jsonify_error(error), error.code

    current_app.logger.error(error)

    return _jsonify_error(InternalServerError()), 500


class FlaskRestly(object):
    _app = None
    _error_handler = None

    def __init__(self, app=None):
        get_blueprints_storage().clear()
        get_metadata_storage().clear()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes FlaskRestAPI

        :param app: Flask application
        :type app: Flask
        """

        if not hasattr(app, 'extensions'):
            app.extensions = dict()

        app.extensions['rest-api'] = self

        app.config.setdefault('RESTLY_SERIALIZER', json)
        app.config.setdefault('RESTLY_API_PREFIX', '/api/rest')
        app.config.setdefault('RESTLY_PROTOBUF_MIMETYPE', 'application/x-protobuf')
        app.config.setdefault('RESTLY_RATE_LIMIT_REQUESTS_AMOUNT', 100)
        app.config.setdefault('RESTLY_RATE_LIMIT_WINDOW_SECONDS', 60)

        if self._error_handler is not None:
            app.register_error_handler(Exception, self._error_handler)
        else:
            app.register_error_handler(Exception, api_error_handler)

        app.after_request(inject_rate_limit_headers)

        self._app = app

    def set_custom_error_handler(self, error_handler):
        self._error_handler = error_handler
