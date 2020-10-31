from flask import Blueprint
from ...tools import urls


api = Blueprint('establishment', __name__)


# views
from .views.company import CompanyListCreateView, CompanyRetriveAllView, CompanyRetrieveUpdateDestroyView
from .views.department import DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView, DepartmentAllView


urls.add_url_rule(
    api, 
    CompanyRetrieveUpdateDestroyView, 
    CompanyListCreateView,
    CompanyRetriveAllView,
    DepartmentListCreateView,
    DepartmentRetrieveUpdateDestroyView,
    DepartmentAllView
)
