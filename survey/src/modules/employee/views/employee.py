from .... import models, schemas
from ....tools.views import generics
from flask import current_app
from flask_jwt_extended import jwt_required


class EmployeeListCreateView(generics.ListCreateAPIView):

    route_path = "/department/<int:department_id>/employees"
    route_name = "employee_list_create"

    model_class = models.Employee
    schema_class = schemas.EmployeeSchema

    unique_fields = ("professional_email" ,"email", "username")

    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.department = models.Department.query.filter_by(pk=kwargs.get("department_id")).first_or_404()
        return super().create(*args, **kwargs)

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.BaseUser, **kwargs)

    def perform_create(self, employee):
        employee.role = models.Role.EMPLOYEE
        employee.department = self.department
        super().perform_create(employee)


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/department/<int:department_id>/employee/<int:id>"
    route_name = "employee_retrieve_update_destroy"

    model_class = models.Employee
    schema_class = schemas.EmployeeSchema
    unique_fields = ("professional_email" ,"email", "username" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"department_id": "department_pk", "id": "pk"}

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.BaseUser, **kwargs)
