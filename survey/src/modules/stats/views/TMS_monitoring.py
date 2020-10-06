from .... import models, schemas, db
from ....tools.views import generics
from .. import constants
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user



class DetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/tms_monitoring/details_of_troubles/<int:department_id>"
    route_name = "details_of_troubles"

    IN = 2
    NOT_IN = 1

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
        #print(rows)

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
                sum_area += kpis_row["score"] if kpis_row["category"] not in categories and kpis_row["area"] not in areas else 0
        return sum_area

    def get_object(self, **kwargs):
        kpis = self.get_all_point(**kwargs)

        # back

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

        # upper_body_limbs
        phys_upper_body_limbs_points = self.get_sum(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.SHOULDERS, constants.ELBOW_WIRST_HAND),
            self.IN
        )

        osteo_upper_body_limbs_points = self.get_sum(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.SHOULDERS, constants.ELBOW_WIRST_HAND),
            self.IN
        )

        # lower_body_limbs
        phys_lower_body_limbs_points = self.get_sum(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.HIP, constants.KNEES, constants.LEG_FOOT),
            self.IN
        )

        osteo_lower_body_limbs_points = self.get_sum(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.HIP, constants.KNEES, constants.LEG_FOOT),
            self.IN
        )

        # headache

        phys_headache_points = self.get_sum(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.HEADACHE,),
            self.IN

        )

        osteo_headache_points = self.get_sum(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.HEADACHE,),
            self.IN
        )

        # abdominal_pains

        phys_abdominal_pains_points = self.get_sum(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.ABDOMINAL_PAIN,),
            self.IN

        )

        osteo_abdominal_pains_points = self.get_sum(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.ABDOMINAL_PAIN,),
            self.IN

        )


        phys_points = self.get_sum_category(kpis, (constants.PHYSIOTHERAPY,), self.IN)
        osteo_points = self.get_sum_category(kpis, (constants.OSTEOPATHY,), self.IN)



        return {
            "tms_details_trouble_Back": "{0:.2f}".format((osteo_back_points + phys_back_points) / (phys_points+osteo_points) * 100),
            "tms_details_trouble_UpperBodyLimbs" : "{0:.2f}".format((osteo_upper_body_limbs_points + phys_upper_body_limbs_points) / (phys_points+osteo_points) * 100),
            "tms_details_trouble_LowerBodyLimbs" : "{0:.2f}".format((osteo_lower_body_limbs_points + phys_lower_body_limbs_points) / (phys_points+osteo_points) * 100),
            "tms_details_trouble_Head": "{0:.2f}".format((osteo_headache_points + phys_headache_points) / (phys_points + osteo_points) * 100),
            "tms_details_trouble_Stomach": "{0:.2f}".format((osteo_abdominal_pains_points + phys_abdominal_pains_points) / (phys_points + osteo_points) * 100)

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

class NeedForInterventionTMS(generics.RetrieveAPIView):
    route_path = "/tms_monitoring/need_for_intervention_tms/<int:department_id>"
    route_name = "need_for_intervention_tms"

    IN = 2
    NOT_IN = 1

    def get_all_point(self, **kwargs):
        rows = db.session.query(
            func.sum(models.QuestionCategory.score).label("sum"),
            models.QuestionCategory.category.label("category"),
            func.sum(models.Question.score).label("asum"),
            models.Question.area.label("area"),
            func.sum(models.Employee.pk).label("employee"),
        ). \
            join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
            join(models.Question, models.Question.category_pk == models.QuestionCategory.pk). \
            join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
            join(models.Department, models.Department.pk == models.Employee.department_pk). \
            filter(models.Department.pk == kwargs.get("department_id")). \
            group_by(models.Question.area, models.Employee.pk, models.QuestionCategory.category). \
            all()
        print(rows)

        area = []
        for row in rows:
            area.append({"score": row[2], "employee": row[4], "area": row[3], "score_category": row[0], "category": row[1]})
        return area

    def get_occurancy(self, kpis, areas, categories, condition):
        sum_area = {}
        for kpis_row in kpis:
            if kpis_row["employee"] not in sum_area:
                sum_area[kpis_row["employee"]] = 0
            if condition == self.IN:
                sum_area[kpis_row["employee"]] += kpis_row["score"] if kpis_row["category"] in categories and kpis_row["area"] in areas else 0
            elif condition == self.NOT_IN:
                sum_area[kpis_row["employee"]] += kpis_row["score"] if kpis_row["category"] not in categories and kpis_row["area"] not in areas else 0


        return sum_area

    def get_object(self, **kwargs):
        kpis = self.get_all_point(**kwargs)

        # back

        phys_cervical = self.get_occurancy(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.CERVICAL,),
            self.IN
        )

        osteo_cervical = self.get_occurancy(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.CERVICAL,),
            self.IN
        )
        phys_back_thorax = self.get_occurancy(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.BACK_THORAX,),
            self.IN
        )

        osteo_back_thorax = self.get_occurancy(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.BACK_THORAX,),
            self.IN
        )
        phys_lumber_buttocks = self.get_occurancy(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.LUMBAR_BUTTOCKS,),
            self.IN
        )

        osteo_lumber_buttocks = self.get_occurancy(
            kpis,
            (constants.OSTEOPATHY,),
            (constants.LUMBAR_BUTTOCKS,),
            self.IN
        )


        return {

            "phys_cervical" : phys_cervical,
            "osteo_cervical" : osteo_cervical,
            'phys_back_thorax' : phys_back_thorax,
            'osteo_back_thorax' : osteo_back_thorax,
            'phys_lumber_buttocks' : phys_lumber_buttocks,
            'osteo_lumber_buttocks' : osteo_lumber_buttocks







        }


    def serialize(self, data=[], many=False, schema_class=None):
        return data