from . import api
from ...tools import urls

# views
from .views.employee import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView
from .views.medical_record import MedicalRecordCreateRetrieveView
from .views.employee_invitation import EmployeeInvitationSendMailView, EmployeeInvitationListCreateView, EmployeeInvitationRetrieveUpdateDestroyView


urls.add_url_rule(
    api, 
    EmployeeListCreateView, 
    EmployeeRetrieveUpdateDestroyView,
    MedicalRecordCreateRetrieveView,
    EmployeeInvitationSendMailView,
    EmployeeInvitationListCreateView,
    EmployeeInvitationRetrieveUpdateDestroyView
)
