from .... import models, schemas, db
from ....tools.views import generics
from .. import constants
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user



class DetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/tms_monitoring/details_of_troubles/<int:department_id>"
    route_name = "details_of_troubles"

    IN = 1
    NOT_IN = 2

    def get_all_point(self, **kwargs):
        rows = db.session.query(
            func.sum(models.QuestionCategory.score).label("sum"),
            models.QuestionCategory.category.label("category") ,
            func.sum(models.Question.score).label("asum"),
            models.Question.area.label("area")
        ). \
            join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
            join(models.Question, models.Question.category_pk == models.QuestionCategory.pk). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            group_by(models.Question.area, models.QuestionCategory.category). \
            all()
        print(rows)

        area = []
        for row in rows:
            area.append({"score": row[2], "area": row[3], "score_category": row[0], "category": row[1]})
        return area

    def get_sum(self, kpis, areas, categories, condition):
        sum_area = 0
        for kpis_row in kpis:
            if condition == self.IN:
                sum_area += kpis_row["score"] if kpis_row["category"] in categories and kpis_row["area"] in areas else 0
            elif condition == self.NOT_IN:
                sum_area += kpis_row["score"] if kpis_row["category"] in categories and kpis_row["area"] in areas else 0
        return sum_area

    def get_object(self, **kwargs):
        kpis = self.get_all_point(**kwargs)

        phys_back_points = self.get_sum(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.CERVICAL, constants.LUMBAR_BUTTOCKS , constants.BACK_THORAX),
            self.IN
        )


        osteo_back_points = self.get_sum(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.CERVICAL, constants.LUMBAR_BUTTOCKS, constants.BACK_THORAX),
            self.IN
        )
        print(osteo_back_points)

        psy_points = self.get_sum_category(kpis, (constants.PSYCHOLOGY,), self.IN)
        osteo_points = self.get_sum_category(kpis, (constants.OSTEOPATHY,), self.IN)

        return {
            "formule": "{0:.2f}".format((osteo_back_points + phys_back_points) / (psy_points+osteo_points) * 100)
        }

    def get_sum_category(self, kpis, categories, condition):
        sum_kpis = 0
        for kpis_row in kpis:
            if condition == self.IN:
                sum_kpis += kpis_row["score_category"] if kpis_row["category"] in categories else 0
            elif condition == self.NOT_IN:
                sum_kpis += kpis_row["score_category"] if kpis_row["category"] not in categories else 0
        return sum_kpis

    def serialize(self, data=[], many=False, schema_class=None):
        return data
