from flask_restly.decorator import resource, get, identity
from flask_restly import FlaskRestly
from flask import Flask


def test_should_inject_identity_when_provider_defined_and_has_arg(mocker):
    app = Flask(__name__)
    FlaskRestly(app)

    stub = mocker.stub(name='identity_provider_stub')

    @identity.provider
    def identity_provider():
        stub()

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get_entity(self, identity):
            return identity

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert stub.call_count == 1


def test_should_not_inject_identity_when_provider_defined_and_has_arg(mocker):
    app = Flask(__name__)
    FlaskRestly(app)

    stub = mocker.stub(name='identity_provider_stub')

    @identity.provider
    def identity_provider():
        stub()

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get_entity(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert stub.call_count == 0


def test_should_fail_when_identity_provider_not_defined_and_kwarg_required():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get_entity(self, *, identity):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 500
