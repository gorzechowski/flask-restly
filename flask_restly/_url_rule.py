def _build_route(resource, path):
    parent = resource._parent if resource._parent is not None else None
    route = resource._resource_name + path.rstrip('/')

    while parent is not None:
        route = parent._resource_name + '/<%s_id>/' % parent._resource_name + route

        if getattr(parent, '_parent', None) is not None:
            parent = parent._parent
        else:
            parent = None

    return route


def _build_rule_name(resource, view_name):
    parent = resource._parent if resource._parent is not None else None
    rule_name = '%s:%s' % (resource._resource_name, view_name)

    while parent is not None:
        rule_name = '%s::' % parent._resource_name + rule_name

        if getattr(parent, '_parent', None) is not None:
            parent = parent._parent
        else:
            parent = None

    return rule_name
