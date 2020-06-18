from . import api
from .. import models, schemas
from .. import models, schemas, mail
from ..views import utils, generics
from flask_mail import Message
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user
from datetime import datetime


class ManagerInvitationSendMailView(generics.CreateAPIView):

    message_html = """<h1>Hello {}!<h1>
<h3>{}</h3>
<a href={}>Here is your login link</a>
<br/>
<p>Best Regards,</p>
<p>The Team.</p>
"""
    route_path = "/company/<string:company_id>/send/invitation/manager/<string:manager_id>"
    route_name = "invitation_manager_send_mail"

    decorators = [ jwt_required ]

    schema_class = schemas.ManagerInvitationSchema

    def filter_object(self, model_class=None, **kwargs):
        self.company = models.Company.objects(id__exact=kwargs.get("company_id", None)).first_or_404()
        return self.company.manager_invitations.filter(id=kwargs.get("manager_id", None)).first()

    def create(self, *args, **kwargs):
        invitation = self.get_object( **kwargs )
        invitation.token = invitation.generate_token( kwargs.get("company_id", None) )
        invitation.send_at = datetime.now()
        models.Company.objects(manager_invitations__id__exact=invitation.id).update_one(
            set__manager_invitations__S__token=invitation.token,
            set__manager_invitations__S__send_at=invitation.send_at
        )
        message = Message(subject="Create Password", sender=current_app.config['FLASK_MAIL_SENDER'], recipients=[invitation.email])
        message.html = self.message_html.format(
            invitation.full_name,
            invitation.subject,
            str(current_app.config['REGISTER_LINK']).format(invitation.token)
        )
        mail.send(message=message)

        return self.serialize(invitation, False), 200


class ManagerInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<string:company_id>/invitations/manager"
    route_name = "invitation_manager_list_create"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema
    unique_fields = ("email", )

    lookup_field_and_url_kwarg = {"company_id": "id"}

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return models.Company.objects(manager_invitations__email__exact=kwargs.get("email")).first()

    def filter_objects(self, model_class=None, start=None, offset=None, **kwargs):
        company = self.get_object(model_class=models.Company, **kwargs)
        return company.manager_invitations[start:offset]

    def create(self, *args, **kwargs):
        self.company = self.get_object(model_class=models.Company, **kwargs)
        return super().create(*args, **kwargs)

    def perform_create(self, manager_invitation):
        self.company.manager_invitations.append( manager_invitation )
        self.company.manager_invitations.save()


class ManagerInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<string:company_id>/invitation/manager/<string:manager_id>"
    route_name = "invitation_manager_retrieve_update_destroy"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema
    unique_fields = ("email", )

    lookup_field_and_url_kwarg = {"company_id": "company_id", "manager_id": "manager_id"}

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return self.company.manager_invitations.filter(email=kwargs.get("email")).first()

    def filter_object(self, model_class=None, **kwargs):
        self.company = models.Company.objects(id__exact=kwargs.get("company_id")).first_or_404()
        return self.company.manager_invitations.filter(id=kwargs.get("manager_id")).first()

    def perform_update(self, manager_invitation, manager_invitation_old ):
        models.Company.objects(manager_invitations__id__exact=manager_invitation_old.id).update_one(
            set__manager_invitations__S__email=manager_invitation.email,
            set__manager_invitations__S__full_name=manager_invitation.full_name,
            set__manager_invitations__S__subject=manager_invitation.subject
        )

    def perform_delete(self, manager_invitation):
        manager_invitation.user.delete()
        models.Company.objects(manager_invitations__id__exact=manager_invitation.id).update_one(
            set__manager_invitations=[invitation for invitation in self.company.manager_invitations if not invitation.id == manager_invitation.id] 
        )


utils.add_url_rule(api, ManagerInvitationListCreateView, ManagerInvitationSendMailView, ManagerInvitationRetrieveUpdateDestroyView)
