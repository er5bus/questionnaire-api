from . import api
from .. import models, schemas, db
from .. import models, schemas, mail
from ..views import utils, generics
from flask_mail import Message
from flask import current_app
from flask_jwt_extended import jwt_required, get_current_user
from datetime import datetime
import uuid


class EmployeeInvitationSendMailView(generics.CreateAPIView):

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
    route_path = "/company/<int:company_id>/send/invitation/employee/<int:employee_id>"
    route_name = "invitation_employee_send_mail"

    lookup_field_and_url_kwarg = {"company_id": "company_pk", "employee_id": "pk"}

    decorators = [ jwt_required ]

    model_class= models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema

    @classmethod
    def send_email(cls, invitation):
        message = Message(subject="Create Password", sender=current_app.config['FLASK_MAIL_SENDER'], recipients=[invitation.email])
        message.html = cls.message_html.format(
            invitation.full_name,
            str(current_app.config['REGISTER_LINK']).format(invitation.token),
            invitation.subject,
            str(current_app.config['REGISTER_LINK']).format(invitation.token),
        )
        mail.send(message=message)

    def create(self, *args, **kwargs):
        invitation = self.perform_update(**kwargs)
        self.send_email(invitation)
        return self.serialize(invitation, False), 200

    def perform_update(self, **kwargs):
        invitation = self.get_object( **kwargs )
        invitation.token = uuid.uuid4()
        invitation.send_at = datetime.now()
        db.session.add(invitation)
        db.session.commit()
        return invitation


class EmployeeInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/company/<int:company_id>/invitations/employee"
    route_name = "invitation_employee_list_create"

    model_class = models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema
    #unique_fields = ("email", )

    lookup_field_and_url_kwarg = {"company_id": "company_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.company = models.Company.query.filter_by(pk=kwargs.get('company_id')).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, employee_invitation):
        employee_invitation.company = self.company
        employee_invitation.token = uuid.uuid4()
        super().perform_create(employee_invitation)
        EmployeeInvitationSendMailView.send_email(employee_invitation)


class EmployeeInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/company/<int:company_id>/invitation/employee/<int:employee_id>"
    route_name = "invitation_employee_retrieve_update_destroy"

    model_class = models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema
    #unique_fields = ("email", )

    lookup_field_and_url_kwarg = {"company_pk": "company_pk", "employee_id": "pk"}

    decorators = [ jwt_required ]


utils.add_url_rule(api, EmployeeInvitationListCreateView, EmployeeInvitationSendMailView, EmployeeInvitationRetrieveUpdateDestroyView)
