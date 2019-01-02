from flask_restly._url_rule import _build_rule_name, _build_route


def test_should_build_proper_rule_name_from_single_resource():
    class Resource:
        _resource_name = 'resource'
        _parent = None

    rule_name = _build_rule_name(Resource(), 'doSomething')

    assert rule_name == 'resource:doSomething'


def test_should_build_proper_rule_name_from_nested_resources():
    class Grand:
        _resource_name = 'grand'
        _parent = None

    class Parent:
        _resource_name = 'parent'
        _parent = Grand

    class Child:
        _resource_name = 'child'
        _parent = Parent

    rule_name = _build_rule_name(Child(), 'doSomething')

    assert rule_name == 'grand::parent::child:doSomething'


def test_should_build_proper_route_from_single_resource():
    class Resource:
        _resource_name = 'resource'
        _parent = None

    route = _build_route(Resource(), '/<id>')

    assert route == 'resource/<id>'


def test_should_build_proper_route_from_nested_resources():
    class Grand:
        _resource_name = 'grand'
        _parent = None

    class Parent:
        _resource_name = 'parent'
        _parent = Grand

    class Child:
        _resource_name = 'child'
        _parent = Parent

    route = _build_route(Child(), '/<id>')

    assert route == 'grand/<grand_id>/parent/<parent_id>/child/<id>'
