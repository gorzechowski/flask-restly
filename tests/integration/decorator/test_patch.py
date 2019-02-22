from flask_restly.decorator import resource, patch
from flask_restly import FlaskRestly
from flask import Flask
import json


def test_should_return_204_code_when_content_is_not_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @patch('/')
        def create(self):
            pass

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.patch('/api/rest/v1/test', data=json.dumps(dict()), content_type='application/json')
        assert response.status_code == 204
        assert response.get_json() is None


def test_should_return_200_code_when_content_is_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @patch('/')
        def create(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.patch('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}
