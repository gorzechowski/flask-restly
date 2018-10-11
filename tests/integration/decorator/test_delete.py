from flask_restly.decorator import resource, delete
from flask_restly import FlaskRestly
from flask import Flask


def test_should_return_204_code_when_content_is_not_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @delete('/')
        def delete(self):
            pass

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.delete('/api/rest/v1/test')
        assert response.status_code == 204
        assert response.get_json() is None


def test_should_return_200_code_when_content_is_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @delete('/')
        def delete(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.delete('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}


def test_should_return_204_code_when_content_is_not_provided_and_action_is_queued():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @delete('/', queued=True)
        def delete(self):
            pass

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.delete('/api/rest/v1/test')
        assert response.status_code == 204
        assert response.get_json() is None


def test_should_return_202_code_when_content_is_provided_and_action_is_queued():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @delete('/', queued=True)
        def delete(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.delete('/api/rest/v1/test')
        assert response.status_code == 202
        assert response.get_json() == {}

