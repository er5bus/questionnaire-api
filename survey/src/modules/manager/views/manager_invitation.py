from .... import models, schemas, mail, db
from ....tools.views import generics
from flask_mail import Message
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user
from datetime import datetime
import uuid


class ManagerInvitationSendMailView(generics.CreateAPIView):

    message_html = """<h1>Hello {}!</h1>

<a href={}>Here is your login link</a>
<br/>

<p>{}</p>
<br />
<p> If Login link does not work {}</p>
<br/>
<p>Best Regards,</p>
<p>The Team.</p>
"""
    route_path = "/company/<int:company_id>/manager-invitation/<int:invitation_id>/send"
    route_name = "invitation_manager_send_mail"

    lookup_field_and_url_kwarg = {"company_id": "company_pk", "invitation_id": "pk"}

    decorators = [ jwt_required ]

    model_class= models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema

    @classmethod
    def send_email(cls, invitation):
        with mail.connect() as conn:
            for user_invitation in invitation.invitations:
                message = Message(subject="Create Password", sender=current_app.config['FLASK_MAIL_SENDER'], recipients=[user_invitation.email])
                message.html = cls.message_html.format(
                    user_invitation.full_name,
                    str(current_app.config['REGISTER_LINK']).format(invitation.token),
                    invitation.subject,
                    str(current_app.config['REGISTER_LINK']).format(invitation.token),
                )
                conn.send(message=message)

    def create(self, *args, **kwargs):
        invitation = self.regenerate_token(**kwargs)
        self.send_email(invitation)
        return self.serialize(invitation, False), 200

    def regenerate_token(self, **kwargs):
        invitation = self.get_object( **kwargs )
        invitation.token = uuid.uuid4()
        invitation.send_at = datetime.now()
        db.session.add(invitation)
        db.session.commit()
        return invitation


class ManagerInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<int:company_id>/manager-invitations"
    route_name = "invitation_manager_list_create"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema

    unique_fields = ("email", )


    lookup_field_and_url_kwarg = {"company_id": "company_pk"}

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.InvitationInfo, **kwargs)

    def validate_unique(self, instance):
        for user_invitation in instance.invitations:
            super().validate_unique(instance=user_invitation)

    def create(self, *args, **kwargs):
        self.company = models.Company.query.filter_by(pk=kwargs.get('company_id')).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, manager_invitation):
        manager_invitation.company = self.company
        super().perform_create(manager_invitation)
        ManagerInvitationSendMailView.send_email(manager_invitation)


class ManagerInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<int:company_id>/manager-invitation/<int:manager_id>"
    route_name = "invitation_manager_retrieve_update_destroy"

    model_class = models.ManagerInvitation
    schema_class = schemas.ManagerInvitationSchema

    lookup_field_and_url_kwarg = {"company_id": "company_pk", "manager_id": "pk"}

    unique_fields = ("email", )

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.InvitationInfo, **kwargs)

    def validate_unique(self, instance, current_object = None):
        for user_invitation in instance.invitations:
            super().validate_unique(instance=user_invitation)
