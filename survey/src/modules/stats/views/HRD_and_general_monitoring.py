from .... import models, schemas, db
from ....tools.views import generics
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user


class NeedForInterventionView(generics.RetrieveAPIView):

    route_path = "/need_for_intervention/<int:department_id>"
    route_name = "need_for_intervention_list"
    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    schema_class = schemas.QuestionCategorySchema
    #decorators = [ jwt_required ]

    def get_object(self, **kwargs):
        rows = db.session.query(models.Questionnaire).\
            with_entities(func.sum(models.QuestionCategory.score), models.QuestionCategory.category). \
            join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            group_by(models.QuestionCategory.category).all()

        result = []
        for row in rows:
            result.append({ "score": row[0], "category": row[1]})
        return result

    def serialize(self, data=[], many=False, schema_class=None):
        return { "data": data}

