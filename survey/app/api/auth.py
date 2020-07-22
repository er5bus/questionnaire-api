from . import api
from .. import models, schemas, jwt
from ..views import generics , utils
from mongoengine.queryset.visitor import Q
from flask import request, abort, current_app
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


@api.before_app_first_request
def before_first_request_func():
    try:
        root = models.Account.objects.get(username__exact=current_app.config['ROOT_USERNAME'])
    except models.Account.DoesNotExist:
        root = models.Account()
        root.username = current_app.config['ROOT_USERNAME']
        root.password = current_app.config['ROOT_PASSWORD']
        root.role = models.Role.ADMIN
        root.save()


blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@jwt.user_loader_callback_loader
def user_loader_callback_loader(jwt_identity):
    if ObjectId.is_valid(jwt_identity):
        return models.Account.objects(id=jwt_identity).first_or_404()
    return None


class InvitationView(generics.RetrieveAPIView):
    route_path = "/auth/invitation/<string:token>"
    route_name = "invitation"

    model_class = models.ManagerInvitation

    lookup_field_and_url_kwarg = {"token": "token"}

    def extract_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf8'))
        except BadData:
            abort(404)
        else:
            return data

    def filter_object(self, model_class=None, **kwargs):
        data = self.extract_token(kwargs.get("token"))
        if data.get('invitation') == 'manager':
            self.schema_class = schemas.ManagerInvitationSchema
            company = models.Company.objects(id__exact=data.get("company_id", None)).first_or_404()
            invitation = company.manager_invitations.filter(id=data.get("id", None)).first()
            if invitation and not invitation.is_created:
                return invitation
        return None


class AccountRegisterView(generics.CreateAPIView, generics.OptionsAPIView):

    route_path = "/auth/register/<string:token>"
    route_name = "user_register"

    model_class = models.Account
    schema_class = schemas.AccountSchema

    unique_fields = ('email', 'username')

    access_token = None

    def extract_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf8'))
        except BadData:
            abort(404)
        else:
            return data

    def create (self, *args, **kwargs):
        self.data = self.extract_token(kwargs.get("token"))
        (response, code) = super().create(self, *args, **kwargs)
        return {**response, "access_token": self.access_token }, code

    def perform_create(self, user):
        company = models.Company.objects(id__exact=self.data.get("company_id", None)).first_or_404()
        if company and self.data.get('invitation', None) == 'manager':
            user.role = models.Role.MODERATOR
            user.company = company
            super().perform_create(user)
            models.Company.objects(manager_invitations__id__exact=self.data.get('id', None)).update_one(
                set__manager_invitations__S__is_created=True,
                set__manager_invitations__S__account=user,
            )
        self.access_token = create_access_token(identity=str(user.id))


class AccountLoginView(generics.CreateAPIView, generics.OptionsAPIView):
    route_path = "/auth/login"
    route_name = "user_login"

    def post(self, *args, **kwargs):
        username_or_email = request.json.get("username_or_email", None)
        password = request.json.get("password", None)
        try:
            current_user = models.Account.objects.get(Q(email__exact=username_or_email) | Q(username__exact=username_or_email)) if password or email else None
            if current_user and current_user.check_password(password):
                data = schemas.AccountSchema(many=False).dump(current_user)
                return {**data ,"access_token": create_access_token(identity=str(current_user.id))}, 200
        except models.Account.DoesNotExist:
            pass
        return abort(400, {"Oops": "Invalid email or password."})


class AccountLogoutView(generics.CreateAPIView):

    route_path = "/auth/logout"
    route_name = "user_logout"

    decorators = [jwt_required]

    def post(self, *args, **kwargs):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


utils.add_url_rule(api, AccountRegisterView, InvitationView, AccountLoginView, AccountLogoutView)
