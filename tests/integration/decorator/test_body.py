from flask_restly.decorator import resource, post
from flask_restly import FlaskRestly
from flask import Flask
import json


def test_should_return_200_code_and_given_body_when_body_declared_and_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @post('/')
        def get_entity(self, body):
            return body

    with app.app_context():
        SomeResource()

    body = {'foo': 'bar'}

    with app.test_client() as client:
        response = client.post('/api/rest/v1/test', data=json.dumps(body), content_type='application/json')
        assert response.status_code == 200
        assert response.get_json() == body


def test_should_return_400_code_when_body_declared_but_not_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @post('/')
        def get_entity(self, body):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.post('/api/rest/v1/test')
        assert response.status_code == 400
