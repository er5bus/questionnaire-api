from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required


class ManagerListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<int:company_id>/managers"
    route_name = "manager_list_create"

    model_class = models.Manager
    schema_class = schemas.ManagerSchema

    unique_fields = ("professional_email" , "email", "username")

    lookup_field_and_url_kwarg = {"company_id": "company_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.company = models.Company.query.filter_by(pk=kwargs.get("company_id")).first_or_404()
        return super().create(*args, **kwargs)

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.BaseUser, **kwargs)

    def perform_create(self, manager):
        manager.role = models.Role.MANAGER
        manager.company = self.company
        super().perform_create(manager)


class ManagerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<int:company_id>/manager/<int:id>"
    route_name = "manager_retrieve_update_destroy"

    model_class = models.Manager
    schema_class = schemas.ManagerSchema
    unique_fields = ("professional_email" ,"email", "username" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"company_id": "company_pk", "id": "pk"}

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.BaseUser, **kwargs)


utils.add_url_rule(api, ManagerListCreateView, ManagerRetrieveUpdateDestroyView)
