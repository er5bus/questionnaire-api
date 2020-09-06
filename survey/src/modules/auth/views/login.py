from .... import models, schemas, jwt, db
from ....tools.views import generics
from flask import request, abort
from sqlalchemy import or_
from flask_jwt_extended import create_access_token


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
            return { **data ,"access_token": create_access_token(identity=str(current_user.pk))}, 200
        return abort(400, {"Oops": "Invalid email or password."})
