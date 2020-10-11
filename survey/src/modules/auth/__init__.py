from ...tools import urls
from flask import Blueprint


api = Blueprint('auth', __name__)

# errors 
from . import errors

# views
from .views.login import BaseUserLoginView
from .views.logout import BaseUserLogoutView
from .views.register import BaseUserRegisterView
from .views.invitation import InvitationView


urls.add_url_rule(
    api,
    BaseUserRegisterView,
    InvitationView,
    BaseUserLoginView,
    BaseUserLogoutView
)
