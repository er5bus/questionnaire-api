from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class ErgonomicsDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/ergonomics-monitoring/details-of-troubles/<int:department_id>"
    route_name = "details_of_troubles_ergonomics"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category(kwargs.get("department_id"))

        ergonomics_points = tools.get_sum_by_category(kpis, (constants.ERGONOMICS,), tools.IN)
        osteo_physio_points = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.IN)
        all_points_except_osteo_physio = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.NOT_IN)
        all_points_all_areas = (osteo_physio_points / 2) + all_points_except_osteo_physio

        ergonomics_result = (ergonomics_points / all_points_all_areas) * 100
        return {
            "SumOfTotalPointsOfAllAreas": "{0:.2f}".format(all_points_all_areas),
            "ergonomics": ergonomics_result,
        }


class ErgonomicsNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/ergonomics-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_ergonomics"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(kwargs.get("department_id"))

        # back
        ergonomics_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.ERGONOMICS,),
            tools.IN
        )

        return ergonomics_need_for_intervention
