from flask_restly.decorator import get, post, put, patch, delete, queued, body, auth
import inspect


def test_get_decorated_method_should_have_proper_arguments_signature():
    @get('')
    def get_entity(id, some, test):
        pass

    inspection = inspect.getfullargspec(get_entity)

    assert inspection.args == ['id', 'some', 'test']


def test_post_decorated_method_should_have_proper_arguments_signature():
    @post('')
    def get_entity(id, some, test):
        pass

    inspection = inspect.getfullargspec(get_entity)

    assert inspection.args == ['id', 'some', 'test']


def test_put_decorated_method_should_have_proper_arguments_signature():
    @put('')
    def get_entity(id, some, test):
        pass

    inspection = inspect.getfullargspec(get_entity)

    assert inspection.args == ['id', 'some', 'test']


def test_patch_decorated_method_should_have_proper_arguments_signature():
    @patch('')
    def get_entity(id, some, test):
        pass

    inspection = inspect.getfullargspec(get_entity)

    assert inspection.args == ['id', 'some', 'test']


def test_delete_decorated_method_should_have_proper_arguments_signature():
    @delete('')
    def get_entity(id, some, test):
        pass

    inspection = inspect.getfullargspec(get_entity)

    assert inspection.args == ['id', 'some', 'test']


def test_queued_decorated_method_should_have_proper_arguments_signature():
    class SomeResource:
        @queued
        def get_entity(self, id, some, test):
            pass

    inspection = inspect.getfullargspec(SomeResource().get_entity)

    assert inspection.args == ['self', 'id', 'some', 'test']


def test_body_decorated_method_should_have_proper_arguments_signature():
    class SomeResource:
        @body()
        def get_entity(self, id, some, test):
            pass

    inspection = inspect.getfullargspec(SomeResource().get_entity)

    assert inspection.args == ['self', 'id', 'some', 'test']


def test_auth_provider_decorated_method_should_have_proper_arguments_signature():
    @auth.provider
    def auth_provider(some, test):
        pass

    inspection = inspect.getfullargspec(auth_provider)

    assert inspection.args == ['some', 'test']


def test_auth_unauthorized_decorated_method_should_have_proper_arguments_signature():
    @auth.unauthorized
    def unauthorized(some, test):
        pass

    inspection = inspect.getfullargspec(unauthorized)

    assert inspection.args == ['some', 'test']
