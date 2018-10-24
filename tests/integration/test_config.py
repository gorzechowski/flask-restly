from flask_restly.decorator import resource, get
from flask_restly import FlaskRestly
from flask import Flask
import pytest


@pytest.mark.parametrize("api_prefix,route", [
    ('api', '/api/v1/test'),
    ('/api', '/api/v1/test'),
    ('api/', '/api/v1/test'),
    ('/api/', '/api/v1/test'),
    ('api/rest', '/api/rest/v1/test'),
    ('/api/rest', '/api/rest/v1/test'),
    ('api/rest/', '/api/rest/v1/test'),
    ('/api/rest/', '/api/rest/v1/test'),

])
def test_should_serialize_given_response_to_json(api_prefix, route):
    app = Flask(__name__)

    app.config['RESTLY_API_PREFIX'] = api_prefix

    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get(route)
        assert response.status_code == 200
