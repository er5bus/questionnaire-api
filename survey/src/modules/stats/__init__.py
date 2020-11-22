from flask import Blueprint


api = Blueprint('stats', __name__)


from ...tools import urls

# views
from .views.HRD_and_general_monitoring import HRDNeedForInterventionView, HRDBreakdownOfFailuresView
from .views.TMS_monitoring import TMSDetailsOfTroublesView, TMSNeedForInterventionView
from .views.RPS_monitoring import RPSDetailsOfTroublesView, RPSNeedForInterventionView
from .views.nutrition_monitoring import NutritionDetailsOfTroublesView, NutritionNeedForInterventionView
from .views.ergonomics_monitoring import ErgonomicsDetailsOfTroublesView, ErgonomicsNeedForInterventionView
from .views.physical_activity_monitoring import PhysicalActivityDetailsOfTroublesView, PhysicalActivityNeedForInterventionView
from .views.export_csv import ExportCSVView


urls.add_url_rule(
    api,
    HRDNeedForInterventionView,
    HRDBreakdownOfFailuresView,
    TMSDetailsOfTroublesView,
    TMSNeedForInterventionView,
    RPSNeedForInterventionView,
    RPSDetailsOfTroublesView,
    NutritionDetailsOfTroublesView, 
    NutritionNeedForInterventionView,
    ErgonomicsDetailsOfTroublesView, 
    ErgonomicsNeedForInterventionView,
    PhysicalActivityDetailsOfTroublesView, 
    ExportCSVView,
    PhysicalActivityNeedForInterventionView
)
