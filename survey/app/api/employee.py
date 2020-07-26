from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required


class EmployeeListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<int:company_id>/employees"
    route_name = "employee_list_create"

    model_class = models.Employee
    schema_class = schemas.EmployeeSchema

    unique_fields = ("email", "username")

    lookup_field_and_url_kwarg = {"company_id": "company_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.company = models.Company.query.filter_by(pk=kwargs.get("company_id")).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, employee):
        employee.role = models.Role.EMPLOYEE
        employee.company = self.company
        super().perform_create(employee)


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/employee/<int:id>"
    route_name = "employee_retrieve_update_destroy"

    model_class = models.Employee
    schema_class = schemas.EmployeeSchema
    unique_fields = ("email", "employeename" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView)
