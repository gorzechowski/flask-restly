from flask import request


def default_key_resolver(group, _):
    if group is None:
        group = request.endpoint

    headers = request.headers.getlist('X-Forwarded-For')
    if headers:
        ip = headers[0]
    else:
        ip = request.remote_addr

    return "__".join([ip, group])


def inject_rate_limit_headers(response):
    try:
        requests, remaining, reset = request.rate_limit_headers
    except (AttributeError, ValueError):
        return response
    else:
        headers = response.headers
        headers.add('X-RateLimit-Limit', requests)
        headers.add('X-RateLimit-Remaining', remaining)
        headers.add('X-RateLimit-Reset', reset)

        return response
