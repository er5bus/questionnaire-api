from . import api
from ...tools import urls

# views
from .views.questionnaire import QuestionnaireListView, QuestionnaireListCreateView
from .views.question_history import QuestionHistoryCreateRetrieveView


urls.add_url_rule(
    api, 
    QuestionnaireListView, 
    QuestionnaireListCreateView,
    QuestionHistoryCreateRetrieveView
)
