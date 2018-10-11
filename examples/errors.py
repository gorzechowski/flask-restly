from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get
from flask_restly.exception import NotFound, BadRequest


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<int:id>')
    def get_employee(self, id):
        if id > 1:
            raise NotFound
            # raise NotFound('Custom message')

        return dict(id=int(id))

    @get('/')
    def get_employees(self):
        raise BadRequest


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
