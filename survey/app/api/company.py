from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user


class CompanyListCreateView(generics.ListCreateAPIView):

    route_path = "/companies"
    route_name = "company_list_create"

    model_class = models.Company
    schema_class = schemas.CompanySchema
    unique_fields = ("name", "universal_name" )

    decorators = [ jwt_required ]

    def perform_create(self, company):
        company.author = get_current_user()
        company.save()


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<string:id>"
    route_name = "company_retrieve_update_destroy"

    model_class = models.Company
    schema_class = schemas.CompanySchema
    unique_fields = ("name", "universal_name" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, CompanyListCreateView, CompanyRetrieveUpdateDestroyView)
