from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user


class NutritionDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/nutrition-monitoring/details-of-troubles/<int:department_id>"
    route_name = "details_of_troubles_nutrition"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category_and_employee(kwargs.get("department_id"))

        all_employees = queries.get_all_employee_of_department(kwargs.get("department_id"))
        answered = tools.get_sum_by_category_and_employee_where_score(kpis, (constants.MEDICINE, ), tools.IN, tools.LESS_THAN, 50)
        other = all_employees - answered
        
        answered_result = (answered / all_employees) * 100
        others_result = (other/ all_employees) * 100
        return {
            "SumOfTotalEmployees": "{0:.2f}".format(all_employees),
            "answered": answered_result,
            "others": others_result,
        }


class NutritionNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/nutrition-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_nutrition"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(kwargs.get("department_id"))

        # back
        nutrition_need_for_intervention = tools.get_recurrence_category_by_employee(
            kpis,
            (constants.MEDICINE,),
            tools.IN
        )

        return nutrition_need_for_intervention
