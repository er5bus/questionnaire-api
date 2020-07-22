from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required


class EmployeeListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<string:company_id>/employees"
    route_name = "employee_list_create"

    model_class = models.Account
    schema_class = schemas.EmployeeSchema

    unique_fields = ("email", "username")

    lookup_field_and_url_kwarg = {"company_id": "id"}

    decorators = [ jwt_required ]

    def filter_objects(self, model_class=None, start=None, offset=None, **kwargs):
        company = self.get_object(model_class=models.Company, **kwargs)
        return company.employees[start:offset]

    def create(self, *args, **kwargs):
        self.company = self.get_object(model_class=models.Company, **kwargs)
        return super().create(*args, **kwargs)

    def perform_create(self, employee):
        employee_account = models.Account()
        employee_account.username = employee.username
        employee_account.email = employee.email
        employee_account.password = employee.password
        employee_account.role = models.Role.EMPLOYEE
        employee_account.company = self.company
        #employee_account.user = employee
        employee_account.save()

        employee.account = employee_account
        self.company.employees.append( employee )
        self.company.employees.save()


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    route_path = "/employee/<string:id>"
    route_name = "employee_retrieve_update_destroy"

    model_class = models.Account
    schema_class = schemas.AccountSchema
    unique_fields = ("email", "employeename" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView)
