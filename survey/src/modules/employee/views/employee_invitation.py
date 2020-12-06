from .... import models, schemas, mail, db
from ....tools.views import generics
from flask_mail import Message
from flask import current_app, render_template
from flask_jwt_extended import jwt_required, get_current_user
from datetime import datetime


class EmployeeInvitationSendMailView(generics.CreateAPIView):

    message_html_template = 'invitation-template.html'
    route_path = "/department/<int:department_id>/employee-invitation/<int:invitation_id>/send"
    route_name = "invitation_employee_send_mail"

    lookup_field_and_url_kwarg = {"department_id": "department_pk", "invitation_id": "pk"}

    decorators = [ jwt_required ]

    model_class= models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema

    @classmethod
    def send_email(cls, invitation):
        with mail.connect() as conn:
            for user_invitation in invitation.invitations:
                message = Message(subject="Create Password", sender=current_app.config['FLASK_MAIL_SENDER'], recipients=[user_invitation.email])
                message.html = render_template(cls.message_html_template, 
                    full_name=user_invitation.full_name,
                    URL=str(current_app.config['REGISTER_LINK']).format(invitation.token),
                    subject=invitation.subject
                )
                conn.send(message=message)

    def create(self, *args, **kwargs):
        invitation = EmployeeInvitationSendMailView.regenerate_token(self.get_object(**kwargs))
        EmployeeInvitationSendMailView.send_email(invitation)
        return self.serialize(invitation, False), 200

    @classmethod
    def regenerate_token(cls, invitation):
        import uuid
        invitation.token = uuid.uuid4()
        invitation.send_at = datetime.now()
        db.session.add(invitation)
        db.session.commit()
        return invitation


class EmployeeInvitationListCreateView(generics.ListCreateAPIView):

    route_path = "/department/<int:department_id>/employee-invitations"
    route_name = "invitation_employee_list_create"

    model_class = models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema

    unique_fields = ("email", )


    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.InvitationInfo, **kwargs)

    def validate_unique(self, instance):
        for user_invitation in instance.invitations:
            super().validate_unique(instance=user_invitation)

    def create(self, *args, **kwargs):
        self.department = models.Department.query.filter_by(pk=kwargs.get('department_id')).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, employee_invitation):
        employee_invitation.department = self.department
        employee_invitation = EmployeeInvitationSendMailView.regenerate_token(employee_invitation)
        EmployeeInvitationSendMailView.send_email(employee_invitation)


class EmployeeInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/department/<int:department_id>/employee-invitation/<int:employee_id>"
    route_name = "invitation_employee_retrieve_update_destroy"

    model_class = models.EmployeeInvitation
    schema_class = schemas.EmployeeInvitationSchema

    lookup_field_and_url_kwarg = {"department_id": "department_pk", "employee_id": "pk"}

    unique_fields = ("email", )

    decorators = [ jwt_required ]

    def filter_unique_object(self, model_class=None, **kwargs):
        return super().filter_unique_object(model_class=models.InvitationInfo, **kwargs)

    def validate_unique(self, instance):
        for user_invitation in instance.invitations:
            super().validate_unique(instance=user_invitation)
