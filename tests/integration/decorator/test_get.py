from flask_restly.decorator import resource, get
from flask_restly import FlaskRestly
from flask import Flask


def test_should_return_200_code_with_content():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/<int:id>')
        def get_entity(self, id):
            return dict(id=id)

        @get('/')
        def get_entities(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}

        response = client.get('/api/rest/v1/test/1')
        assert response.status_code == 200
        assert response.get_json() == {'id': 1}
