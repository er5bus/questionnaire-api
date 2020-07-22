from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user


class AccountListCreateView(generics.ListCreateAPIView):

    route_path = "/users"
    route_name = "user_list_create"

    model_class = models.Account
    schema_class = schemas.AccountSchema
    unique_fields = ("email", "username" )

    decorators = [ jwt_required ]

    def perform_create(self, user):
        user.author = get_current_user()
        user.save( validate=False )


class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/user/<string:id>"
    route_name = "user_retrieve_update_destroy"

    model_class = models.Account
    schema_class = schemas.AccountSchema
    unique_fields = ("email", "username" )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, AccountListCreateView, AccountRetrieveUpdateDestroyView)
