from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, identity


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@identity.provider
def identity_provider():
    return dict(id=123)


@resource(name='employees')
class EmployeesResource:
    @get('/<int:id>')
    def get_employee(self, id, identity):
        return dict(employee_id=id, identity=identity)

    @get('/')
    def get_employees(self, identity):
        return dict(
            entites=[
                dict(id=1),
                dict(id=2)
            ],
            identity=identity
        )


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
