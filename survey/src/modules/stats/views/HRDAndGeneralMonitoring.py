from .... import models, schemas, db
from ....tools.views import generics
from flask_jwt_extended import jwt_required, get_current_user


class NeedForInterventionView(generics.ListAPIView):

    route_path = "/need_for_intervention/<int:department_id>"
    route_name = "need_for_intervention_list"

    model_class = models.Questionnaire
    schema_class = schemas.QuestionnaireSchema

    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    #decorators = [ jwt_required ]

    def get_object_query(self, **kwargs):
        return db.session.query(models.Questionnaire). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            order_by(models.Questionnaire.date.desc())

