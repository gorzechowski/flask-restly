from flask import Flask, make_response
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<id>')
    def get_employee(self, id):
        return make_response('Requested id: {}'.format(id))


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
