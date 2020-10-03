from .... import models, schemas, db
from ....tools.views import generics
from .. import constants
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user


class NeedForInterventionView(generics.RetrieveAPIView):

    route_path = "/hrd_general_monitoring/need_for_intervention/<int:department_id>"
    route_name = "need_for_intervention_list"
    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    schema_class = schemas.QuestionCategorySchema
    #decorators = [ jwt_required ]

    def get_object(self, **kwargs):
        rows = db.session.query(func.sum(models.QuestionCategory.score).label("sum"), models.QuestionCategory.category.label("category")). \
            join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            group_by(models.QuestionCategory.category).all()

        kpis = []
        gpt = 0
        for row in rows:
            gpt += row[0] if row[1] in (constants.PHYSIOTHERAPY, constants.OSTEOPATHY, constants.ERGONOMICS) else 0
            kpis.append({ "score": row[0], "category": row[1]})

        gpt = gpt / 3 if gpt > 0 else 0
        return { "KPIS": kpis, "GPT": gpt }

    def serialize(self, data=[], many=False, schema_class=None):
        return data


class BreakdownOfFailures(generics.RetrieveAPIView):

    route_path = "/hrd_general_monitoring/breakdown_of_failures/<int:department_id>"
    route_name = "breakdown_of_failures"

    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    IN = "not_in"
    NOT_IN = "in"

    def get_all_point(self, **kwargs):
        rows = db.session.query(func.sum(models.QuestionCategory.score).label("sum"), models.QuestionCategory.category.label("category")). \
            join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            group_by(models.QuestionCategory.category).all()

        kpis = []
        gpt = 0
        for row in rows:
            gpt += row[1] if row[1] in (constants.PHYSIOTHERAPY, constants.OSTEOPATHY, constants.ERGONOMICS) else 0
            kpis.append({ "score": row[0], "category": row[1]})
        return kpis

    def get_sum(self, kpis, categories, condition=IN):
        sum_kpis = 0
        for kpis_row in kpis: 
            if condition == IN:
                sum_kpis += kpis_row["score"] if kpis_row["category"] in categories else 0
            elif condition ==NOT_IN:
                sum_kpis += kpis_row["score"] if kpis_row["category"] not in categories else 0
        return sum_kpis
        

    def get_object(self, **kwargs):
        kpis = self.get_all_point(**kwargs)

        psy_points = self.get_sum(kpis, (constants.PHYSIOTHERAPY, ), IN) 
        osteo_physio_points = self.get_sum(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), IN)
        all_points_except_osteo_physio = self.get_sum(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), NOT_IN)
        all_points_all_areas = ((osteo_physio_points or 1) / 2) + all_points_except_osteo_physio

        return {
            "SumOfTotalPointsOfAllAreas": "{}%".format(all_points_all_areas),
            "TMS": "{}%".format(1/2 * (osteo_physio_points) / (all_points_all_areas) * 100),
            "RPS": "1%",#(sum of all psy points) / total points of all areas,
            "ergonomics": "1%",#sum of ergo points / total points = (211/1334) * 100 = 16%
            "nutrition": "1%",#sum of dietitian points / total points = (123/1334) * 100 = 9%
            "PhysicalActivity": "1%"#sum of coach points / total points = (45/1334) * 100 = 3%
        }


    def serialize(self, data=[], many=False, schema_class=None):
        return data
