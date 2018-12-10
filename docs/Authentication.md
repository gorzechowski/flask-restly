# Authentication

Identity provider will give You an ability to authenticate requests

## Usage

```python
from flask_restly.decorator import identity
```

Implement identity provider function:

```python
@identity.provider
def identity_provider():
    return dict(id=1)
```

And then use this identity in view functions:

```python
@resource(name='some')
class SomeResource():
    @get('/')
    def get_some(self, identity):
        print(identity)
        return dict()
```

NOTE: If executed view function do not declare `identity` argument, then identity provider function is not executed.
