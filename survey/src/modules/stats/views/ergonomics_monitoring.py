from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class ErgonomicsDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/ergonomics-monitoring/details-of-troubles/<signed_int:department_id>"
    route_name = "details_of_troubles_ergonomics"
    
    fake_data = { -1: 30, 20: 10, 21: 20, 22: 60, 23: 5 }

    def get_object(self, **kwargs):
        try:
            department_id = kwargs.get("department_id")
            kpis = queries.get_all_point_by_department_group_by_category(department_id)

            ergonomics_points = tools.get_sum_by_category(kpis, (constants.ERGONOMICS,), tools.IN)
            osteo_physio_points = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.IN)
            all_points_except_osteo_physio = tools.get_sum_by_category(kpis, (constants.OSTEOPATHY, constants.PHYSIOTHERAPY), tools.NOT_IN)
            all_points_all_areas = (osteo_physio_points / 2) + all_points_except_osteo_physio
            ergonomics_result = (ergonomics_points / all_points_all_areas) * 100
        except ZeroDivisionError:
           ergonomics_result = 0
           all_points_all_areas = 0

        if department_id in self.fake_data:
            ergonomics_result = self.fake_data[department_id]
        
        return {
            "SumOfTotalPointsOfAllAreas": "{0:.2f}".format(all_points_all_areas),
            "ergonomics": ergonomics_result,
        }


class ErgonomicsNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/ergonomics-monitoring/need-for-intervention/<signed_int:department_id>"
    route_name = "need_for_intervention_ergonomics"

    fake_data = { 
        -1: {tools.PREVENTIVE: 40, tools.MODERATE: 30, tools.IMPORTANT: 20, tools.URGENT: 10},  
        20: {tools.PREVENTIVE: 40, tools.MODERATE: 30, tools.IMPORTANT: 20, tools.URGENT: 10}, 
        21: {tools.PREVENTIVE: 30, tools.MODERATE: 30, tools.IMPORTANT: 20, tools.URGENT: 20}, 
        22: {tools.PREVENTIVE: 10, tools.MODERATE: 20, tools.IMPORTANT: 20, tools.URGENT: 50}, 
        23: {tools.PREVENTIVE: 60, tools.MODERATE: 20, tools.IMPORTANT: 10, tools.URGENT: 10},
    }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(department_id)

        # back
        ergonomics_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.ERGONOMICS,),
            tools.IN
        )

        if department_id in self.fake_data:
            ergonomics_need_for_intervention = self.fake_data[department_id]

        return ergonomics_need_for_intervention
