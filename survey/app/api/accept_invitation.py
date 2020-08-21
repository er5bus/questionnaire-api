from . import api
from .. import models, schemas, jwt, db
from ..views import generics , utils
from flask import request, abort, current_app
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required


class InvitationView(generics.RetrieveAPIView):
    route_path = "/auth/invitation/<string:token>"
    route_name = "invitation"

    model_class = models.BaseInvitation
    schema_class = schemas.BaseInvitationSchema

    lookup_field_and_url_kwarg = {"token": "token"}

    def get_object(self, **kwargs):
        return super().get_object(**kwargs, is_expired=False)


class BaseUserRegisterView(generics.CreateAPIView, generics.OptionsAPIView):

    route_path = "/auth/register/<string:token>"
    route_name = "user_register"

    model_class = models.BaseUser
    schema_class = schemas.BaseUserSchema

    unique_fields = ("professional_email", "email", "username")

    invitation = None
    access_token = None

    def create (self, *args, **kwargs):
        self.invitation = models.BaseInvitation.query.filter_by(token=kwargs.get("token")).first_or_404()

        if isinstance(self.invitation, models.ManagerInvitation):
            self.schema_class = schemas.ManagerSchema
        elif isinstance(self.invitation, models.EmployeeInvitation):
            self.schema_class = schemas.EmployeeSchema

        (response, code) = super().create(self, *args, **kwargs)
        self.set_token_expiration()
        return {**response, "access_token": self.access_token }, code

    def check_professional_email(self, professional_email):
        for invitation in self.invitation.invitations:
            if professional_email == invitation.email:
                return True
        return False

    def set_token_expiration(self):
        if len(self.invitation.accounts) == len(self.invitation.invitations):
            self.invitation.is_expired = True
            db.session.add(self.invitation)
            db.session.commit()

    def create_manger(self, manager):
        manager.role = models.Role.MANAGER
        manager.invitation = self.invitation
        manager.company = self.invitation.company

    def create_employee(self, employee):
        employee.role = models.Role.EMPLOYEE
        employee.invitation = self.invitation
        employee.department = self.invitation.department

    def perform_create(self, user):
        if not self.check_professional_email(user.professional_email) \
                or not isinstance(self.invitation, (models.ManagerInvitation, models.EmployeeInvitation)) or self.invitation.is_expired:
            abort(400, "Invitation is either expired or professional email not valid")

        if isinstance(self.invitation, models.ManagerInvitation):
            self.create_manger(user)
        elif isinstance(self.invitation, models.EmployeeInvitation):
            self.create_employee(user)
 
        super().perform_create(user)
        self.access_token = create_access_token(identity=str(user.pk))


utils.add_url_rule(api, BaseUserRegisterView, InvitationView)
