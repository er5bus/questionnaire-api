from . import api
from ...tools import urls

# views
from .views.HRD_and_general_monitoring import NeedForInterventionView, BreakdownOfFailuresView


urls.add_url_rule(
    api,
    NeedForInterventionView,
    BreakdownOfFailuresView
)
