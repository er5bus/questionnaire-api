from .... import models, schemas, db
from ....tools.views import generics
from flask import current_app, jsonify, Response
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
        super().perform_create(company)


class CompanyRetriveAllView(generics.RetrieveAPIView):

    route_path = "/companies/all"
    route_name = "companies_retrieve_all"

    decorators = [ jwt_required ]

    model_class = models.Company

    def get_object(self, model_class=None, **kwargs):
        return models.Company.objects.all()

    def serialize(self, companies, many=False):
        items = []
        for company in companies:
            items.append({"value": company.pk, "label": company.name })
        return { "results": items }


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<string:id>"
    route_name = "company_retrieve_update_destroy"

    model_class = models.Company
    schema_class = schemas.CompanySchema
    unique_fields = ("name", "universal_name" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "pk"}
