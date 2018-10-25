# Authorization

By default `flask-restly` assumes that **client is authorized**

If authorization provider return `False`, then `Forbidden` exception is raised.

## Usage

```python
from flask_restly.decorator import auth
```

To implement Your custom authorization function:

```python
@auth.provider
def authorize():
    return True
```

In some cases authorization should not be verified for particular endpoint(s):

```python
@resource(name='some')
class SomeResource():
    @get('/')
    @auth.unauthorized
    def can_be_not_authorized(self):
        return

```
