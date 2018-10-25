# Flask-RESTly

[![Build Status](https://travis-ci.org/gorzechowski/flask-restly.svg?branch=master)](https://travis-ci.org/gorzechowski/flask-restly)
[![Latest version](https://img.shields.io/pypi/v/flask-restly.svg)](https://pypi.org/project/flask-restly)
[![Python versions](https://img.shields.io/pypi/pyversions/flask-restly.svg)](https://pypi.org/project/flask-restly)

## Features

* Decorators-based routing
* JSON and Protobuf built-in serialization
* Custom serializer support
* Automatic REST-like response codes

## Todo

* HATEOAS
* ...and few more :)

## Usage

Please see [examples](/examples) for more details.

## Quick start

```
pip install flask-restly
```

By default `flask-restly` uses JSON serializer.

```python
from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, delete


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<id>')
    def get_employee(self, id):
        return dict(id=int(id))

    @get('/')
    def get_employees(self):
        return dict(entites=[
            dict(id=1),
            dict(id=2)
        ])

    @delete('/<id>')
    def delete_employee(self, **kwargs):
        return


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
```

```bash
$ python main.py
* Serving Flask app "main" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: 210-167-642
* Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```

## Protobuf

```
# employee.proto

syntax = "proto3";

message Employee {
    int32 id = 1;
    string name = 2;
}
```

```python
from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, body, post
from flask_restly.serializer import protobuf
from employee_pb2 import Employee

app = Flask(__name__)

app.config['RESTLY_SERIALIZER'] = protobuf

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<int:id>')
    @body(Employee)
    def get_employee(self, id):
        return dict(id=id, name="some name")

    @post('/')
    @body(Employee, Employee)
    # @body(outgoing=Employee, incoming=Employee)
    def create_employee(self, body):
        # print(body)
        return dict(id=1, name=body.get('name'))


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
```
