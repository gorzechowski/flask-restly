from flask_restly.decorator import resource, get, auth
from flask_restly import FlaskRestly
from flask import Flask


def test_should_return_200_code_if_authorized():
    app = Flask(__name__)
    FlaskRestly(app)

    @auth.provider
    def authorize():
        return True

    @resource(name='test')
    class SomeResource:
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 200
        assert response.get_json() == {'id': 1}


def test_should_return_403_code_if_not_authorized():
    app = Flask(__name__)
    FlaskRestly(app)

    @auth.provider
    def authorize():
        return False

    @resource(name='test')
    class SomeResource:
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 403


def test_should_return_200_code_if_authorization_is_skipped():
    app = Flask(__name__)
    FlaskRestly(app)

    @auth.provider
    def authorize():
        return False

    @resource(name='test')
    class SomeResource:
        @get('/<int:id>')
        @auth.unauthorized
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 200
        assert response.get_json() == {'id': 1}
