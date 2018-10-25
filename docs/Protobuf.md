# Protobuf

Compile below message with `protoc`:

```
# employee.proto

syntax = "proto3";

message Employee {
    int32 id = 1;
    string name = 2;
}
```

Then use generated code in Your application:

```python
from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, body, post
from flask_restly.serializer import protobuf
# generated message
from employee_pb2 import Employee

app = Flask(__name__)

app.config['RESTLY_SERIALIZER'] = protobuf

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<int:id>')
    @body(Employee)
    # @body(outgoing=Employee)
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
