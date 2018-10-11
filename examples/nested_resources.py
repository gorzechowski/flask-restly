from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='companies')
class CompaniesResource:
    @get('/<id>')
    def get_company(self, id):
        return dict(id=int(id))

    @get('/')
    def get_companies(self):
        return dict(companies=[
            dict(id=1),
            dict(id=2)
        ])


@resource(name='employees', parent=CompaniesResource)
class EmployeesResource:
    @get('/')
    def get_employees(self, **kwargs):
        company_id = int(kwargs.get('companies_id'))

        return dict(employees=[
            dict(id=1, company_id=company_id),
            dict(id=2, company_id=company_id)
        ])


with app.app_context():
    EmployeesResource()
    CompaniesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
