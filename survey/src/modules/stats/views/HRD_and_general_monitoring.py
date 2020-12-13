from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries
from flask_jwt_extended import jwt_required, get_current_user


class HRDNeedForInterventionView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/need-for-intervention/<signed_int:department_id>"
    route_name = "need_for_intervention_hrd"

    decorators = [ jwt_required ]

    fake_kpis_data = { 
        -1: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  20 },
            { "category": constants.ERGONOMICS, "category_score":  20 },
            { "category": constants.MEDICINE, "category_score":  20 },
            { "category": constants.PSYCHOLOGY, "category_score":  20 },
            { "category": constants.COACH, "category_score":  20 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  20 },
            { "category": constants.STOPP_WORKING, "category_score":  20 },
        ],
        20: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  20 },
            { "category": constants.ERGONOMICS, "category_score":  20 },
            { "category": constants.MEDICINE, "category_score":  20 },
            { "category": constants.PSYCHOLOGY, "category_score":  20 },
            { "category": constants.COACH, "category_score":  20 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  20 },
            { "category": constants.STOPP_WORKING, "category_score":  20 },
        ], 
        21: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  20 },
            { "category": constants.ERGONOMICS, "category_score":  20 },
            { "category": constants.MEDICINE, "category_score":  20 },
            { "category": constants.PSYCHOLOGY, "category_score":  20 },
            { "category": constants.COACH, "category_score":  20 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  20 },
            { "category": constants.STOPP_WORKING, "category_score":  20 },
        ], 22: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  20 },
            { "category": constants.ERGONOMICS, "category_score":  20 },
            { "category": constants.MEDICINE, "category_score":  20 },
            { "category": constants.PSYCHOLOGY, "category_score":  20 },
            { "category": constants.COACH, "category_score":  20 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  20 },
            { "category": constants.STOPP_WORKING, "category_score":  20 },
        ], 23: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  20 },
            { "category": constants.ERGONOMICS, "category_score":  20 },
            { "category": constants.MEDICINE, "category_score":  20 },
            { "category": constants.PSYCHOLOGY, "category_score":  20 },
            { "category": constants.COACH, "category_score":  20 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  20 },
            { "category": constants.STOPP_WORKING, "category_score":  20 },
        ]
    }
    fake_gpt_data = { -1: 50, 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_question_completed_data = { -1: 30, 20: 20, 21: 10, 22: 60, 23: 5 }

    def get_object(self, **kwargs): 

        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category(department_id)
        gpt = tools.get_sum_by_category(kpis, (constants.PHYSIOTHERAPY, constants.OSTEOPATHY, constants.ERGONOMICS), tools.IN)
        gpt = gpt / 3 if gpt > 0 else 0
        question_completed = gpt

        if department_id in self.fake_kpis_data:
            kpis = self.fake_kpis_data[department_id]

        if department_id in self.fake_gpt_data:
            gpt = self.fake_gpt_data[department_id]

        if department_id in self.fake_question_completed_data:
            question_completed = self.fake_question_completed_data[department_id]
            
        return { "kpis": kpis, "questionCompleted": question_completed, "gpt": float("{0:.2f}".format(gpt)) }


class HRDBreakdownOfFailuresView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/breakdown-of-failures/<signed_int:department_id>"
    route_name = "breakdown_of_failures_hrd"

    fake_tms_data = { -1: 20, 20: 60, 21: 50, 22: 60, 23: 33 }
    fake_rps_data = { -1: 40, 20: 60, 21: 50, 22: 40, 23: 25 }
    fake_ergonomics_data = { -1: 60, 20: 10, 21: 5, 22: 60, 23: 5 }
    fake_nutrition_data = { -1: 30, 20: 20, 21: 20, 22: 45, 23: 5 }
    fake_physical_activity_data = { -1: 40, 20: 10, 21: 50, 22: 40, 23: 40 }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category(department_id)

        psy_points=tools.get_sum_by_category(kpis, (constants.PSYCHOLOGY,), tools.IN)
        ergonomics_points = tools.get_sum_by_category(kpis, (constants.ERGONOMICS,), tools.IN)
        coach_points = tools.get_sum_by_category(kpis, (constants.COACH,), tools.IN)
        nutrition_points = tools.get_sum_by_category(kpis, (constants.NUTRITION,), tools.IN)
        osteo_physio_points = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.IN)
        all_points_except_osteo_physio = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.NOT_IN)
        all_points_all_areas = ((osteo_physio_points or 1) / 2) + all_points_except_osteo_physio

        tms = 1/2 * (osteo_physio_points) / (all_points_all_areas) * 100
        rps = (psy_points / all_points_all_areas) * 100
        ergonomics = (ergonomics_points / all_points_all_areas) * 100
        nutrition = (nutrition_points / all_points_all_areas) * 100
        physical_activity = (coach_points / all_points_all_areas) * 100

        if department_id in self.fake_tms_data:
            tms = self.fake_tms_data[department_id]

        if department_id in self.fake_rps_data:
            rps = self.fake_rps_data[department_id]

        if department_id in self.fake_ergonomics_data:
            ergonomics = self.fake_ergonomics_data[department_id]

        if department_id in self.fake_nutrition_data:
            nutrition = self.fake_nutrition_data[department_id]

        if department_id in self.fake_physical_activity_data:
            physical_activity = self.fake_physical_activity_data[department_id]

        return {
            "sumOfTotalPointsOfAllAreas": all_points_all_areas,
            "TMS": tms,
            "RPS": rps,
            "ergonomics": ergonomics,
            "nutrition": nutrition,
            "physicalActivity": physical_activity
        }

