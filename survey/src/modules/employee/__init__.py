from flask import Blueprint
from ...tools import urls

api = Blueprint('employee', __name__)

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
