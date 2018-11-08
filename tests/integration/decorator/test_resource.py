from flask_restly.decorator import resource, get
from flask_restly import FlaskRestly
from flask import Flask


def test_should_register_resource():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}


def test_should_register_resources_with_same_method_names():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return dict()

    @resource(name='test2')
    class SomeResource2:
        @get('/')
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()
        SomeResource2()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}

        response = client.get('/api/rest/v1/test2')
        assert response.status_code == 200
        assert response.get_json() == {}


def test_should_register_resource_with_subresource_with_same_method_names():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='parent')
    class SomeResource:
        @get('/')
        def get(self):
            return dict()

    @resource(name='child', parent=SomeResource)
    class SomeResource2:
        @get('/')
        def get(self, **kwargs):
            return dict()

    with app.app_context():
        SomeResource()
        SomeResource2()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/parent')
        assert response.status_code == 200
        assert response.get_json() == {}

        response = client.get('/api/rest/v1/parent/1/child')
        assert response.status_code == 200
        assert response.get_json() == {}


def test_should_register_different_api_version_resources_with_same_method_names():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return dict()

    @resource(name='test', version=2)
    class SomeResource2:
        @get('/')
        def get(self):
            return dict()

    with app.app_context():
        SomeResource()
        SomeResource2()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        assert response.status_code == 200
        assert response.get_json() == {}

        response = client.get('/api/rest/v2/test')
        assert response.status_code == 200
        assert response.get_json() == {}


def test_should_register_subresource():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='parent')
    class ParentResource:
        @get('/')
        def get_parent(self):
            return dict()

    @resource(name='child', parent=ParentResource)
    class ChildResource:
        @get('/')
        def get_child(self, parent_id):
            return dict(parent_id=int(parent_id))

    with app.app_context():
        ChildResource()
        ParentResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/parent/1/child')
        assert response.status_code == 200
        data = response.get_json()
        assert data['parent_id'] is 1


def test_should_register_subresource_of_subresource():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='grand')
    class ParentParentResource:
        @get('/')
        def get_grand(self):
            return dict()

    @resource(name='parent', parent=ParentParentResource)
    class ParentResource:
        @get('/')
        def get_parent(self, grand_id):
            return dict(grand_id=int(grand_id))

    @resource(name='child', parent=ParentResource)
    class ChildResource:
        @get('/')
        def get_child(self, grand_id, parent_id):
            return dict(parent_id=int(parent_id), grand_id=int(grand_id))

    with app.app_context():
        ParentParentResource()
        ChildResource()
        ParentResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/grand/1/parent/111/child')
        assert response.status_code == 200
        data = response.get_json()
        assert data['grand_id'] is 1
        assert data['parent_id'] is 111
