from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, rate
from time import time

app = Flask(__name__)

rest = FlaskRestly()
rest.init_app(app)

_requests = dict()


@rate.resolver
def view_rate_limit(key, window, identity):
    try:
        requests, expires = _requests.get(key)

        if expires < int(time()):
            expires = expires + window
            requests = 0
    except (ValueError, TypeError):
        requests = 0
        expires = time() + window

    _requests[key] = (requests + 1, int(expires))

    return _requests.get(key)


@resource(name='employees')
class EmployeesResource:
    @rate.limit(requests=2, window=5)
    @get('/')
    def get_employees(self):
        return dict(entites=[
            dict(id=1),
            dict(id=2)
        ])


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
