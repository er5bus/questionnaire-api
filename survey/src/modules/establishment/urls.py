from . import api
from ...tools import urls

# views
from .views.company import CompanyListCreateView, CompanyRetriveAllView, CompanyRetrieveUpdateDestroyView
from .views.department import DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView


urls.add_url_rule(
    api, 
    CompanyRetrieveUpdateDestroyView, 
    CompanyListCreateView,
    CompanyRetriveAllView,
    DepartmentListCreateView,
    DepartmentRetrieveUpdateDestroyView
)
