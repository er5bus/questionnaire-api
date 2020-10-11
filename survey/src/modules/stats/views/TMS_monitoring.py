from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_current_user


class TMSDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/tms_monitoring/details_of_troubles/<int:department_id>"
    route_name = "details_of_troubles_tms"

    def get_object(self, **kwargs):
        category_and_area_kpis = queries.get_all_point_by_department_group_by_category_and_area(kwargs.get("department_id"))
        category_kpis = queries.get_all_point_by_department_group_by_category(kwargs.get("department_id"))

        # back
        back_points = tools.get_sum_by_category_and_area(
            category_and_area_kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.CERVICAL, constants.LUMBAR_BUTTOCKS , constants.BACK_THORAX),
            tools.IN
        )
        

        # upper_body_limbs
        upper_body_limbs_points = tools.get_sum_by_category_and_area(
            category_and_area_kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.SHOULDERS, constants.ELBOW_WIRST_HAND),
            tools.IN
        )

        # lower_body_limbs
        lower_body_limbs_points = tools.get_sum_by_category_and_area(
            category_and_area_kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HIP, constants.KNEES, constants.LEG_FOOT),
            tools.IN
        )

        # headache
        headache_points = tools.get_sum_by_category_and_area(
            category_and_area_kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HEADACHE,),
            tools.IN

        )

        # abdominal_pains
        abdominal_pains_points = tools.get_sum_by_category_and_area(
            category_and_area_kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.ABDOMINAL_PAIN,),
            tools.IN

        )

        all_points = tools.get_sum_by_category(category_kpis, (constants.PHYSIOTHERAPY, constants.OSTEOPATHY), tools.IN)

        return {
            "backPoints": "{0:.2f}%".format(back_points and all_points and (back_points / all_points * 100)),
            "upperBodyLimbsPoints" : "{0:.2f}%".format(upper_body_limbs_points and all_points and (upper_body_limbs_points / all_points * 100)),
            "lowerBodyLimbsPoints" : "{0:.2f}%".format(lower_body_limbs_points and all_points and (lower_body_limbs_points / all_points * 100)),
            "headachePoints": "{0:.2f}%".format(headache_points and all_points and (headache_points / all_points * 100)),
            "abdominalPainsPoints": "{0:.2f}%".format(abdominal_pains_points and all_points and (abdominal_pains_points / all_points * 100))
        }


class TMSNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/tms_monitoring/need_for_intervention/<int:department_id>"
    route_name = "need_for_intervention_tms"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(kwargs.get("department_id"))

        # back
        cervical = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.CERVICAL,),
            tools.IN
        )

        back_thorax = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.BACK_THORAX,),
            tools.IN
        )

        lumber_buttocks = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY,),
            (constants.LUMBAR_BUTTOCKS,),
            tools.IN
        )

        return {
            "cervical" : cervical,
            "backThorax" : back_thorax,
            "lumberButtocks" : lumber_buttocks,
        }
