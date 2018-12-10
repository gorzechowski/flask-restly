# Decorators

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
