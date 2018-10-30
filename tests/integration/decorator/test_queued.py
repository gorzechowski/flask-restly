from flask_restly.decorator import resource, get, queued
from flask_restly import FlaskRestly
from flask import Flask


def test_should_return_202_code_with_content_when_action_is_queued():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        @queued
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 202
        assert response.get_json() == {}
