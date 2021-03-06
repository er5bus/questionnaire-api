from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class PhysicalActivityDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/physical-activity-monitoring/details-of-troubles/<signed_int:department_id>"
    route_name = "details_of_troubles_physical_activity"

    fake_data = { -1: 33, 20: 10, 21: 10, 22: 60, 23: 5 }

    def get_object(self, **kwargs):
        try:
            department_id = kwargs.get("department_id")
            kpis = queries.get_all_point_by_department_group_by_category(department_id)

            coach_points = tools.get_sum_by_category(kpis, (constants.COACH,), tools.IN)
            osteo_physio_points = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.IN)
            all_points_except_osteo_physio = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.NOT_IN)
            all_points_all_areas = (osteo_physio_points / 2) + all_points_except_osteo_physio

            physical_activity_result = (coach_points / all_points_all_areas) * 100
        except ZeroDivisionError:
            physical_activity_result = 0
            all_points_all_areas = 0

        if department_id in self.fake_data:
            physical_activity_result = self.fake_data[department_id]

        return {
            "sumOfTotalPointsOfAllAreas": "{0:.2f}".format(all_points_all_areas),
            "physicalActivity": physical_activity_result
        }


class PhysicalActivityNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/physical-activity-monitoring/need-for-intervention/<signed_int:department_id>"
    route_name = "need_for_intervention_physical_activity"

    fake_data = {
        -1: {tools.PREVENTIVE: 10, tools.MODERATE: 10, tools.IMPORTANT: 20, tools.URGENT: 60},
        20: {tools.PREVENTIVE: 10, tools.MODERATE: 10, tools.IMPORTANT: 20, tools.URGENT: 60},
        21: {tools.PREVENTIVE: 5, tools.MODERATE: 5, tools.IMPORTANT: 20, tools.URGENT: 70},
        22: {tools.PREVENTIVE: 20, tools.MODERATE: 30, tools.IMPORTANT: 20, tools.URGENT: 30},
        23: {tools.PREVENTIVE: 30, tools.MODERATE: 10, tools.IMPORTANT: 20, tools.URGENT: 40},
    }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(department_id)

        # back
        coach_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.COACH,),
            tools.IN
        )

        if department_id in self.fake_data:
            coach_need_for_intervention = self.fake_data[department_id]

        return coach_need_for_intervention
