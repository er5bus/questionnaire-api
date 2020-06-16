from . import api
from .. import models, schemas, jwt
from ..views import generics , utils
from mongoengine.queryset.visitor import Q
from flask import request, abort, current_app
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required


@api.before_app_first_request
def before_first_request_func():
    try:
        root = models.User.objects.get(username__exact=current_app.config['ROOT_USERNAME'])
    except models.User.DoesNotExist:
        root = models.User()
        root.username = current_app.config['ROOT_USERNAME']
        root.password = current_app.config['ROOT_PASSWORD']
        root.roles = [ models.Role.ADMIN ]
        root.save()


blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@jwt.user_loader_callback_loader
def user_loader_callback_loader(jwt_identity):
    if ObjectId.is_valid(jwt_identity):
        return models.User.objects(id=jwt_identity).first_or_404()
    return None


class UserRegisterView(generics.CreateAPIView, generics.OptionsAPIView):

    route_path = "/auth/register/<string:token>"
    route_name = "user_register"

    model_class = models.User
    schema_class = schemas.UserSchema

    access_token = None

    def create (self, *args, **kwargs):
        (response, code) = super().create(self, *args, **kwargs)
        return {**response, "access_token": self.access_token }, code

    def perform_create(self, instance):
        super().perform_create(instance)
        self.access_token = create_access_token(identity=instance.id)


class UserLoginView(generics.CreateAPIView, generics.OptionsAPIView):
    route_path = "/auth/login"
    route_name = "user_login"

    def post(self, *args, **kwargs):
        username_or_email = request.json.get("username_or_email", None)
        password = request.json.get("password", None)
        try:
            current_user = models.User.objects.get(Q(email__exact=username_or_email) | Q(username__exact=username_or_email)) if password or email else None
            if current_user and current_user.check_password(password):
                data = schemas.UserSchema(many=False).dump(current_user)
                return {**data ,"access_token": create_access_token(identity=str(current_user.id))}, 200
        except models.User.DoesNotExist:
            pass
        return abort(400, {"Oops": "Invalid email or password."})


class UserLogoutView(generics.CreateAPIView):

    route_path = "/auth/logout"
    route_name = "user_logout"

    decorators = [jwt_required]

    def post(self, *args, **kwargs):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


utils.add_url_rule(api, UserRegisterView, UserLoginView, UserLogoutView)
