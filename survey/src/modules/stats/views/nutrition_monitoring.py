from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class NutritionDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/nutrition-monitoring/details-of-troubles/<int:department_id>"
    route_name = "details_of_troubles_nutrition"

    fake_answered_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_others_data = { 20: 10, 21: 10, 22: 60, 23: 5 }

    def get_object(self, **kwargs):
        try:
            department_id = kwargs.get("department_id")
            kpis = queries.get_all_point_by_department_group_by_category_and_employee(department_id)

            all_employees = queries.get_all_employee_of_department(department_id)
            answered = tools.get_sum_by_category_and_employee_where_score(kpis, (constants.NUTRITION, ), tools.IN, tools.LESS_THAN, 50)
            other = all_employees - answered
        
            answered_result = (answered / all_employees) * 100
            others_result = (other/ all_employees) * 100
        except ZeroDivisionError:
            answered_result = 0
            others_result = 0

        if department_id in self.fake_answered_data:
            answered_result = fake_answered_data[department_id]

        if department_id in self.fake_others_data:
            others_result = fake_others_data[department_id]
 
        return {
            "SumOfTotalEmployees": "{0:.2f}".format(all_employees),
            "answered": answered_result,
            "others": others_result,
        }


class NutritionNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/nutrition-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_nutrition"
    
    fake_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(department_id)

        # back
        nutrition_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.NUTRITION,),
            tools.IN
        )

        if department_id in self.fake_data:
            nutrition_need_for_intervention = fake_data[department_id]

        return nutrition_need_for_intervention
