from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class RPSDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/rps-monitoring/details-of-troubles/<signed_int:department_id>"
    route_name = "details_of_troubles_rps"

    fake_data = { -1: 40, 20: 60, 21: 50, 22: 40, 23: 45 }

    def get_object(self, **kwargs):
        try:
            department_id = kwargs.get("department_id")
            kpis = queries.get_all_point_by_department_group_by_category(department_id)

            psy_points=tools.get_sum_by_category(kpis, (constants.PSYCHOLOGY,), tools.IN)
            osteo_physio_points = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.IN)
            all_points_except_osteo_physio = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.NOT_IN)
            all_points_all_areas = (osteo_physio_points / 2) + all_points_except_osteo_physio
            stress = ((psy_points / all_points_all_areas) * 100 )
        except ZeroDivisionError:
            stress = 0
            all_points_all_areas = 0

        if department_id in self.fake_data:
            stress = self.fake_data[department_id]
        
        return {
            "sumOfTotalPointsOfAllAreas": "{0:.2f}".format(all_points_all_areas),
            "stress": stress,
        }


class RPSNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/rps-monitoring/need-for-intervention/<signed_int:department_id>"
    route_name = "need_for_intervention_rps"

    fake_data = {
        -1: {tools.PREVENTIVE: 20, tools.MODERATE: 40, tools.IMPORTANT: 20, tools.URGENT: 20},
        20: {tools.PREVENTIVE: 20, tools.MODERATE: 40, tools.IMPORTANT: 20, tools.URGENT: 20},
        21: {tools.PREVENTIVE: 60, tools.MODERATE: 20, tools.IMPORTANT: 10, tools.URGENT: 10},
        22: {tools.PREVENTIVE: 45, tools.MODERATE: 5, tools.IMPORTANT: 30, tools.URGENT: 20},
        23: {tools.PREVENTIVE: 10, tools.MODERATE: 30, tools.IMPORTANT: 50, tools.URGENT: 20},
    }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(department_id)

        # back
        psy_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.PSYCHOLOGY,),
            tools.IN
        )

        if department_id in self.fake_data:
            psy_need_for_intervention = self.fake_data[department_id]

        return psy_need_for_intervention
