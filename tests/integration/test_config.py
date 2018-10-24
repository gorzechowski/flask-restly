from flask_restly.decorator import resource, get, body
from flask_restly.serializer import protobuf
from flask_restly import FlaskRestly
from flask import Flask
from tests.fixtures.entity_pb2 import Entity
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


def test_should_use_custom_protobuf_mime_type():
    expected_type = 'application/pb'

    app = Flask(__name__)

    app.config['RESTLY_SERIALIZER'] = protobuf
    app.config['RESTLY_PROTOBUF_MIMETYPE'] = expected_type

    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        @body(Entity)
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.headers.get('Content-Type') == expected_type
