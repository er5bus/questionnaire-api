from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user


class ManagerInvitationSendMailView(generics.CreateAPIView):

    message_txt = """Hello {}!
{}
<a href={}>Here is your login link</a>

Best Regards,
The Team.
"""
    route_path = "/invitations/manager"
    route_name = "invitation_manager_list_create"


class ManagerInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/invitations/manager"
    route_name = "invitation_manager_list_create"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema
    unique_fields = ("email", )

    decorators = [ jwt_required ]

    def perform_create(self, manager_invitation):
        manager_invitation.generate_token()
        manager_invitation.author = get_current_user()
        manager_invitation.save()


class ManagerInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/invitation/manager/<string:id>"
    route_name = "invitation_manager_retrieve_update_destroy"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema
    unique_fields = ("email", )

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"id": "id"}


utils.add_url_rule(api, ManagerInvitationListCreateView, ManagerInvitationRetrieveUpdateDestroyView)
