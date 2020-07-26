from . import api
from .. import models, schemas, jwt, db
from ..views import generics , utils
from flask import request, abort, current_app
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


@api.before_app_first_request
def before_first_request_func():
    root = models.BaseUser.query.filter_by(username=current_app.config['ROOT_USERNAME']).one_or_none()
    if not root:
        root = models.BaseUser()
        root.username = current_app.config['ROOT_USERNAME']
        root.password = current_app.config['ROOT_PASSWORD']
        root.role = models.Role.ADMIN
        db.session.add(root)
        db.session.commit()


blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@jwt.user_loader_callback_loader
def user_loader_callback_loader(jwt_identity):
    return models.BaseUser.query.filter_by(pk=jwt_identity).first_or_404()


class InvitationView(generics.RetrieveAPIView):
    route_path = "/auth/invitation/<string:token>"
    route_name = "invitation"

    model_class = models.BaseInvitation
    schema_class = schemas.BaseInvitationSchema

    lookup_field_and_url_kwarg = {"token": "token"}

class BaseUserRegisterView(generics.CreateAPIView, generics.OptionsAPIView):

    route_path = "/auth/register/<string:token>"
    route_name = "user_register"

    model_class = models.BaseUser
    schema_class = schemas.BaseUserSchema

    unique_fields = ('email', 'username')

    invitation = None
    access_token = None

    def create (self, *args, **kwargs):
        self.invitation = models.BaseInvitation.query.filter_by(token=kwargs.get("token")).first_or_404()
        (response, code) = super().create(self, *args, **kwargs)
        return {**response, "access_token": self.access_token }, code

    def perform_create(self, user):
        user.role = models.Role.MODERATOR
        user.invitation = self.invitation
        user.company = self.invitation.company
        self.invitation.token=None
        self.invitation.is_created=True
        db.session.add(user)
        db.session.add(self.invitation)
        db.session.commit()
        self.access_token = create_access_token(identity=str(user.pk))


class BaseUserLoginView(generics.CreateAPIView, generics.OptionsAPIView):
    route_path = "/auth/login"
    route_name = "user_login"

    def post(self, *args, **kwargs):
        username_or_email = request.json.get("username_or_email", None)
        password = request.json.get("password", None)
        current_user = models.BaseUser.query.filter(or_(models.BaseUser.email==username_or_email, models.BaseUser.username==username_or_email)).one_or_none()
        if current_user and current_user.check_password(password):
            data = schemas.BaseUserSchema(many=False).dump(current_user)
            return {**data ,"access_token": create_access_token(identity=str(current_user.pk))}, 200
        return abort(400, {"Oops": "Invalid email or password."})


class BaseUserLogoutView(generics.CreateAPIView):

    route_path = "/auth/logout"
    route_name = "user_logout"

    decorators = [jwt_required]

    def post(self, *args, **kwargs):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


utils.add_url_rule(api, BaseUserRegisterView, InvitationView, BaseUserLoginView, BaseUserLogoutView)
