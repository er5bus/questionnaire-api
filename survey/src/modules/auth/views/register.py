from .... import models, schemas, db
from flask import abort
from flask_jwt_extended import create_access_token
from ....tools.views import generics


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
            self.model_class = models.Manager
        elif isinstance(self.invitation, models.EmployeeInvitation):
            self.schema_class = schemas.EmployeeSchema
            self.model_class = models.Employee

        super().create(self, *args, **kwargs)
        
        if isinstance(self.invitation, models.ManagerInvitation):
            self.create_manger(self.user)
        elif isinstance(self.invitation, models.EmployeeInvitation):
            self.create_employee(self.user)
        
        data = self.serialize(self.user)
        self.set_token_expiration()
        return { **data, "access_token": create_access_token(identity=str(self.user.pk)) }, 201

    def check_professional_email(self, professional_email):
        for invitation in self.invitation.invitations:
            if professional_email.lower() == invitation.email.lower():
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
        super().perform_create(manager)

    def create_employee(self, employee):
        employee.role = models.Role.EMPLOYEE
        employee.invitation = self.invitation
        employee.department = self.invitation.department
        super().perform_create(employee)

    def perform_create(self, user):
        if not self.check_professional_email(user.professional_email) \
                or not isinstance(self.invitation, (models.ManagerInvitation, models.EmployeeInvitation)) or self.invitation.is_expired:
            abort(400, "Invitation is either expired or professional email not valid")
        self.user = user
