from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user


class CompanyInvitationSendMailView(generics.CreateAPIView):

    message_txt = """Hello {}!
{}
<a href={}>Here is your login link</a>

Best Regards,
The Team.
"""
    route_path = "/invitations/company"
    route_name = "invitation_company_list_create"


class CompanyInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/invitations/company"
    route_name = "invitation_company_list_create"

    model_class = models.CompanyInvitation
    schema_class = schemas.CompanyInvitationSchema
    unique_fields = ("email", )

    decorators = [ jwt_required ]

    def perform_create(self, company_invitation):
        company_invitation.generate_token()
        company_invitation.author = get_current_user()
        company_invitation.save()


class CompanyInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/invitation/company/<string:id>"
    route_name = "invitation_company_retrieve_update_destroy"

    model_class = models.CompanyInvitation
    schema_class = schemas.CompanyInvitationSchema
    unique_fields = ("email", )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, CompanyInvitationListCreateView, CompanyInvitationRetrieveUpdateDestroyView)
