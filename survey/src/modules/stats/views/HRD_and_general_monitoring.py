from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries
from flask_jwt_extended import jwt_required, get_current_user


class HRDNeedForInterventionView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_hrd"

    decorators = [ jwt_required ]

    fake_kpis_data = { 
        20: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  10 },
            { "category": constants.ERGONOMICS, "category_score":  10 },
            { "category": constants.MEDICINE, "category_score":  50 },
            { "category": constants.PSYCHOLOGY, "category_score":  60 },
            { "category": constants.COACH, "category_score":  10 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  60 },
            { "category": constants.STOPP_WORKING, "category_score":  0 },
        ], 
        21: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  40 },
            { "category": constants.ERGONOMICS, "category_score":  5 },
            { "category": constants.MEDICINE, "category_score":  60 },
            { "category": constants.PSYCHOLOGY, "category_score":  50 },
            { "category": constants.COACH, "category_score":  50 },
            { "category": constants.NUTRITION, "category_score":  20 },
            { "category": constants.OSTEOPATHY, "category_score":  40 },
            { "category": constants.STOPP_WORKING, "category_score":  0 },
        ], 22: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  40 },
            { "category": constants.ERGONOMICS, "category_score":  60 },
            { "category": constants.MEDICINE, "category_score":  80 },
            { "category": constants.PSYCHOLOGY, "category_score":  40 },
            { "category": constants.COACH, "category_score":  40 },
            { "category": constants.NUTRITION, "category_score":  45 },
            { "category": constants.OSTEOPATHY, "category_score":  60 },
            { "category": constants.STOPP_WORKING, "category_score":  0 },
        ], 23: [
            { "category": constants.PHYSIOTHERAPY, "category_score":  10 },
            { "category": constants.ERGONOMICS, "category_score":  5 },
            { "category": constants.MEDICINE, "category_score":  45 },
            { "category": constants.PSYCHOLOGY, "category_score":  30 },
            { "category": constants.COACH, "category_score":  40 },
            { "category": constants.NUTRITION, "category_score":  5 },
            { "category": constants.OSTEOPATHY, "category_score":  45 },
            { "category": constants.STOPP_WORKING, "category_score":  0 },
        ]
    }
    fake_gpt_data = { 20: 10, 21: 10, 22: 60, 23: 5 }

    def get_object(self, **kwargs): 
    
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category(department_id)
        gpt = tools.get_sum_by_category(kpis, (constants.PHYSIOTHERAPY, constants.OSTEOPATHY, constants.ERGONOMICS), tools.IN)
        gpt = gpt / 3 if gpt > 0 else 0

        if department_id in self.fake_kpis_data:
            kpis = self.fake_kpis_data[department_id]

        if department_id in self.fake_gpt_data:
            gpt = self.fake_gpt_data[department_id]
            
        return { "KPIS": kpis, "GPT": float("{0:.2f}".format(gpt)) }


class HRDBreakdownOfFailuresView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/breakdown-of-failures/<int:department_id>"
    route_name = "breakdown_of_failures_hrd"

    fake_tms_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_rps_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_ergonomics_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_nutrition_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_physical_activity_data = { 20: 10, 21: 10, 22: 60, 23: 5 }

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

