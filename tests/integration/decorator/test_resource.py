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
        assert data['parent_id'] == 1


def test_should_register_nested_subresources():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='resource')
    class Resource:
        @get('/')
        def get(self):
            return dict()

    @resource(name='subresource1', parent=Resource)
    class Subresource1:
        @get('/')
        def get(self, **kwargs):
            pass

    @resource(name='subresource2', parent=Subresource1)
    class Subresource2:
        @get('/')
        def get(self, **kwargs):
            pass

    @resource(name='subresource3', parent=Subresource2)
    class Subresource3:
        @get('/')
        def get(self, **kwargs):
            pass

    @resource(name='subresource4', parent=Subresource3)
    class Subresource4:
        @get('/')
        def get(self, resource_id, subresource1_id, subresource2_id, subresource3_id):
            return dict(
                resource_id=int(resource_id),
                subresource1_id=int(subresource1_id),
                subresource2_id=int(subresource2_id),
                subresource3_id=int(subresource3_id),
            )

    with app.app_context():
        Resource()
        Subresource1()
        Subresource2()
        Subresource3()
        Subresource4()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/resource/1/subresource1/23/subresource2/45/subresource3/67/subresource4')
        assert response.status_code == 200
        data = response.get_json()
        assert data['resource_id'] == 1
        assert data['subresource1_id'] == 23
        assert data['subresource2_id'] == 45
        assert data['subresource3_id'] == 67
