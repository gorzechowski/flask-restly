from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get


app = Flask(__name__)

# json is default serializer
# from flask_restly.serializer import json
# app.config['RESTLY_SERIALIZER'] = json

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<id>', serialize=lambda result, _: str(result.get('id')))
    def get_employee(self, id):
        return dict(id=int(id))

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
