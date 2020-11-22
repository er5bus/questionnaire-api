from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries
from flask_jwt_extended import jwt_required, get_current_user


class HRDNeedForInterventionView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_hrd"

    decorators = [ jwt_required ]

    def get_object(self, **kwargs): 
        kpis = queries.get_all_point_by_department_group_by_category(kwargs.get("department_id"))
        gpt = tools.get_sum_by_category(kpis, (constants.PHYSIOTHERAPY, constants.OSTEOPATHY, constants.ERGONOMICS), tools.IN)
        gpt = gpt / 3 if gpt > 0 else 0
        return { "KPIS": kpis, "GPT": float("{0:.2f}".format(gpt)) }


class HRDBreakdownOfFailuresView(generics.RetrieveAPIView):

    route_path = "/hrd-general-monitoring/breakdown-of-failures/<int:department_id>"
    route_name = "breakdown_of_failures_hrd"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category(kwargs.get("department_id"))

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

        return {
            "sumOfTotalPointsOfAllAreas": all_points_all_areas,
            "TMS": tms,
            "RPS": rps,
            "ergonomics": ergonomics,
            "nutrition": nutrition,
            "physicalActivity": physical_activity
        }

