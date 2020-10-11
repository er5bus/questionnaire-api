from .... import models, schemas, db
from ....tools.views import generics
from flask_jwt_extended import jwt_required, get_current_user


class QuestionnaireListView(generics.ListAPIView):

    route_path = "/questionnaires/<int:department_id>"
    route_name = "questionnaires_list"

    model_class = models.Questionnaire
    schema_class = schemas.QuestionnaireSchema

    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    decorators = [ jwt_required ]

    def get_object_query(self, **kwargs):
        return db.session.query(models.Questionnaire). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            order_by(models.Questionnaire.date.desc())


class QuestionnaireListCreateView(generics.ListCreateAPIView):

    route_path = "/employee/<int:employee_id>/questionnaires"
    route_name = "questionnaires_list_create"

    model_class = models.Questionnaire
    schema_class = schemas.QuestionnaireSchema

    lookup_field_and_url_kwarg = {"employee_id": "employee_pk"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.employee = models.Employee.query.filter_by(pk=kwargs.get("employee_id")).first_or_404()
        return super().create(*args, **kwargs)

    def perform_create(self, questionnaire):
        questionnaire.employee = self.employee
        super().perform_create(questionnaire)
