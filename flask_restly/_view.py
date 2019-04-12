from flask import (
    Response,
    current_app,
    request,
)
from flask_restly._storage import get_metadata_storage
from flask_restly.exception import Forbidden, BadRequest, TooManyRequests


def _view_factory(instance, obj, callback, serialize):
    serializer = current_app.config.get('RESTLY_SERIALIZER')
    deserialize = serializer.deserialize

    if serialize is None:
        serialize = serializer.serialize

    metadata = get_metadata_storage().get(obj.__name__).get(callback.__name__)
    outgoing = metadata.get('outgoing', None)
    incoming = metadata.get('incoming', None)
    skip_auth = metadata.get('skip_authorization', False)
    inject_identity = metadata.get('inject_identity', False)
    inject_body = metadata.get('inject_body', False)
    queued = metadata.get('queued', False)
    auth_provider = get_metadata_storage().get('auth_provider', lambda: True)
    identity_provider = get_metadata_storage().get('identity_provider', None)
    rate_limit_resolver = get_metadata_storage().get('rate_limit_resolver', lambda: None)
    key_resolver = current_app.config.get('RESTLY_RATE_LIMIT_KEY_RESOLVER')
    rating_limit = metadata.get('rating_limit', None)

    def wrapper(*args, **kwargs):
        if not skip_auth and auth_provider() is False:
            raise Forbidden()

        if inject_identity and identity_provider is not None:
            kwargs['identity'] = identity_provider()

        if rating_limit and rate_limit_resolver is not None:
            group = rating_limit.get('group', None)
            requests_limit = rating_limit.get('requests', current_app.config.get('RESTLY_RATE_LIMIT_REQUESTS_AMOUNT'))
            window = rating_limit.get('window', current_app.config.get('RESTLY_RATE_LIMIT_WINDOW_SECONDS'))

            key = key_resolver(group, kwargs.get('identity', None))

            requests_amount, valid_to = rate_limit_resolver(key, window, kwargs.get('identity', None))

            remaining = requests_limit - requests_amount

            if remaining < 0:
                raise TooManyRequests()

            request.rate_limit_headers = (requests_limit, remaining, int(valid_to))

        if inject_body:
            if len(request.get_data()) == 0:
                raise BadRequest("Body is required for given request but was not provided")

            kwargs['body'] = deserialize(request, incoming)

        response, code = callback(instance, *args, **kwargs)

        if isinstance(response, Response):
            return response, response.status_code

        return serialize(response, outgoing) if response != '' else response, code if not queued else 202

    return wrapper
