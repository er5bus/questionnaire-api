from . import api
from .. import models, schemas, jwt, db
from ..views import generics , utils
from flask import request, abort, current_app
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required


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


class BaseUserLoginView(generics.CreateAPIView, generics.OptionsAPIView):
    route_path = "/auth/login"
    route_name = "user_login"

    def post(self, *args, **kwargs):
        username_or_email = request.json.get("username_or_email", None)
        password = request.json.get("password", None)
        current_user = models.BaseUser.query.filter(or_(models.BaseUser.email==username_or_email, models.BaseUser.username==username_or_email)).one_or_none()
        if current_user and current_user.check_password(password):
            if isinstance(current_user, models.Manager):
                data = schemas.ManagerSchema(many=False).dump(current_user)
            elif isinstance(current_user, models.Employee):
                data = schemas.EmployeeSchema(many=False).dump(current_user)
            else:
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


utils.add_url_rule(api, BaseUserLoginView, BaseUserLogoutView)
