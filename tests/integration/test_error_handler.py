from flask_restly.decorator import resource, get
from flask_restly.exception import (
    InternalServerError,
    BadRequest,
    Conflict,
    NotFound,
    NotImplemented,
    NotAcceptable,
    UnprocessableEntity,
    Unauthorized,
    TooManyRequests,
    Forbidden,
)
from flask_restly import FlaskRestly
from flask import Flask
import pytest


@pytest.mark.parametrize("error,expected_error_code,expected_message", [
    (Exception(), 500, InternalServerError.description),
    (InternalServerError(), 500, InternalServerError.description),
    (BadRequest(), 400, BadRequest.description),
    (Conflict(), 409, Conflict.description),
    (NotFound(), 404, NotFound.description),
    (NotImplemented(), 501, NotImplemented.description),
    (NotAcceptable(), 406, NotAcceptable.description),
    (UnprocessableEntity(), 422, UnprocessableEntity.description),
    (Unauthorized(), 401, Unauthorized.description),
    (TooManyRequests(), 429, TooManyRequests.description),
    (Forbidden(), 403, Forbidden.description),
])
def test_should_return_json_when_http_error_raised(error, expected_error_code, expected_message):
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            raise error

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == expected_error_code
        data = response.get_json()
        assert data['error'] == expected_message


def test_should_return_original_error_when_not_api_resource():
    app = Flask(__name__)
    FlaskRestly(app)

    @app.route('/some/url')
    def some_url():
        raise Exception("Some error")

    with app.test_client() as client:
        try:
            client.get('/some/url')
        except Exception as e:
            assert str(e) == 'Some error'


def test_should_use_custom_error_handler():
    app = Flask(__name__)
    api = FlaskRestly()
    api.set_custom_error_handler(lambda error: ('', 201))
    api.init_app(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            raise Exception()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 201
        assert response.get_json() is None
