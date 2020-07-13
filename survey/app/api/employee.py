from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required


class EmployeeListCreateView(generics.CreateAPIView):

    route_path = "/employees"
    route_name = "employee_list_create"

    model_class = models.User
    schema_class = schemas.UserSchema
    unique_fields = ("email", "username")

    decorators = [ jwt_required ]

    def perform_create(self, employee):
        employee.role = models.Role.EMPLOYEE
        employee.save( validate=False )


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/employee/<string:id>"
    route_name = "employee_retrieve_update_destroy"

    model_class = models.User
    schema_class = schemas.UserSchema
    unique_fields = ("email", "employeename" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView)
