from .... import models, schemas
from ....tools.views import generics
from flask import current_app
from flask_jwt_extended import jwt_required


class DepartmentListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<int:company_id>/departments"
    route_name = "department_list_create"

    model_class = models.Department
    schema_class = schemas.DepartmentSchema

    unique_fields = ("name", )

    lookup_field_and_url_kwarg = {"company_id": "company_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.company = models.Company.query.filter_by(pk=kwargs.get("company_id")).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, department):
        department.company = self.company
        super().perform_create(department)


class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<int:company_id>/department/<int:id>"
    route_name = "department_retrieve_update_destroy"

    model_class = models.Department
    schema_class = schemas.DepartmentSchema
    unique_fields = ("name", )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"company_id": "company_pk", "id": "pk"}

