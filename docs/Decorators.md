# Decorators

List of decorators provided by `flask_restly`:

1. auth.provider
1. auth.unauthorized
1. body
1. delete
1. get
1. identity.provider
1. patch
1. post
1. put
1. queued
1. rate.key_resolver
1. rate.limit
1. rate.resolver
1. resource

```python
from flask_restly.decorator import *
```

## Auth and Identity

Decorators from auth and identity modules are described with examples in `Authentication` and `Authorization` docs 

## Rate

Decorators from rate module are described with examples in `RateLimits` docs

## Queued

In some cases You may need to do some job in the background. `@queued` decorator will change response code to 202 - Accepted. This informs API client that request job is done asynchronously.

Example usage: 

```python
from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, post, queued

app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='commands')
class CommandsResource:
    @post('/<int:id>')
    @queued
    def create_command(self, id, body):
        print(body)
        return dict(job_id=id, status="RUNNING")


with app.app_context():
    CommandsResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
```
