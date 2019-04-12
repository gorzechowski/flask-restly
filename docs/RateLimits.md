# Rate limits

Rate limiting defines limits on how many API calls can be made within a specified period of time

`flask-restly` comes with decorators and makes it easier to implement API rating limit

## Usage

```python
from flask_restly.decorator import rate
```

To implement simple rating limit resolver:

```python
@rate.resolver
def view_rate_limit(key, window, identity):
    try:
        requests, expires = _data.get(key)

        if expires < int(time()):
            expires = expires + window
            requests = 0
    except (ValueError, TypeError):
        requests = 0
        expires = time() + window

    _data[key] = (requests + 1, int(expires))

    return _data.get(key)
```

Above example resolver may be tested with `limits` example. Resolver returns tuple or list with a number of already called API requests and expiration timestamp. 

```python
@resource(name='some')
class SomeResource():
    @get('/')
    @rate.limit() # use default settings
    @rate.limit(requests=5, window=30, group='custom_group') # or override them
    def get_something(self):
        return dict()

```

## Rating limits key resolver

By default `flask-restly` is configured with it's own key resolver, which implementation may be found in `flask_restly/_rate.py`.

You may provide custom key resolver function:

```python
from flask import request

@rate.key_resolver
def _custom_key_resolver(group, identity):
    if group is None:
        group = request.endpoint

    return f'{group}.{identity.id}'
```

`group` is a keyword argument provided to `@rate.limit` decorator.

## Configuration

Each view is able to gain it's own properties (requests, window), but You are also able to change default properties:

```python
app.config['RESTLY_RATE_LIMIT_REQUESTS_AMOUNT'] = 3
app.config['RESTLY_RATE_LIMIT_WINDOW_SECONDS'] = 300
```
