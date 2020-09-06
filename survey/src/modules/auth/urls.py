from . import api
from ...tools import urls

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


# errors
from . import errors
