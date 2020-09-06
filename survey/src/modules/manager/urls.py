from . import api
from ...tools import urls

# views
from .views.manager import ManagerListCreateView, ManagerRetrieveUpdateDestroyView
from .views.manager_invitation import ManagerInvitationSendMailView, ManagerInvitationListCreateView, ManagerInvitationRetrieveUpdateDestroyView


urls.add_url_rule(
    api, 
    ManagerListCreateView, 
    ManagerRetrieveUpdateDestroyView,
    ManagerInvitationSendMailView,
    ManagerInvitationListCreateView,
    ManagerInvitationRetrieveUpdateDestroyView
)
