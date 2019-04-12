from flask_restly.decorator import resource, get, rate
from flask_restly import FlaskRestly
from flask import Flask
from time import time


def test_should_return_429_code_if_too_much_requests():
    app = Flask(__name__)
    FlaskRestly(app)

    requests_limit = 2
    _data = dict()

    @rate.resolver
    def view_rate_limit(key, window, _):
        requests = _data.get(key, 0)
        _data[key] = requests + 1

        return _data.get(key, 0), time() + window

    @resource(name='test')
    class SomeResource:
        @rate.limit(requests=requests_limit)
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        for _ in range(requests_limit):
            response = client.get('/api/rest/v1/test/1')
            assert response.status_code == 200

        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 429


def test_should_inject_proper_headers():
    app = Flask(__name__)
    FlaskRestly(app)

    requests_limit = 2
    time_window = 2

    _data = dict()
    now = int(time())

    @rate.resolver
    def view_rate_limit(key, window, _):
        requests = _data.get(key, 0)
        _data[key] = requests + 1

        return _data.get(key, 0), now + window

    @resource(name='test')
    class SomeResource:
        @rate.limit(requests=requests_limit, window=time_window)
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.headers.get('X-RateLimit-Limit', type=int) == requests_limit
        assert response.headers.get('X-RateLimit-Remaining', type=int) == requests_limit - 1
        assert response.headers.get('X-RateLimit-Reset', type=int) == now + time_window


def test_should_use_custom_group_name():
    app = Flask(__name__)
    FlaskRestly(app)

    requests_limit = 2
    group_name = 'test'
    data_group_name = '127.0.0.1__' + group_name

    _data = {
        data_group_name: requests_limit,
    }

    @rate.resolver
    def view_rate_limit(key, window, _):
        requests = _data.get(key, 0)
        _data[key] = requests + 1

        return _data.get(key, 0), time() + window

    @resource(name='test')
    class SomeResource:
        @rate.limit(requests=requests_limit, group=group_name)
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 429


def test_should_use_custom_key_resolver():
    app = Flask(__name__)
    FlaskRestly(app)

    group_name = 'some_custom_key'

    @rate.key_resolver
    def _custom_key_resolver(*_):
        return group_name

    requests_limit = 2

    _data = {
        group_name: requests_limit,
    }

    @rate.resolver
    def view_rate_limit(key, window, _):
        requests = _data.get(key, 0)
        _data[key] = requests + 1

        return _data.get(key, 0), time() + window

    @resource(name='test')
    class SomeResource:
        @rate.limit(requests=requests_limit)
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 429
