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
