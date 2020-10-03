from .auth import api as auth_blueprint
from .employee import api as employee_blueprint
from .establishment import api as establishment_blueprint
from .manager import api as manager_blueprint
from .questionnaire import api as questionnaire_blueprint
from .stats import api as stats_blueprint

api_blueprints = [
    auth_blueprint,
    employee_blueprint,
    establishment_blueprint,
    manager_blueprint,
    questionnaire_blueprint,
    stats_blueprint
]

