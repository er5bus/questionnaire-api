from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class TMSDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/tms-monitoring/details-of-troubles/<int:department_id>"
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

        back_result = back_points and all_points and (back_points / all_points * 100)
        upper_body_limbs_result = upper_body_limbs_points and all_points and (upper_body_limbs_points / all_points * 100)
        lower_body_limbs_result = lower_body_limbs_points and all_points and (lower_body_limbs_points / all_points * 100)
        headache_result = headache_points and all_points and (headache_points / all_points * 100)
        abdominal_pains_result = abdominal_pains_points and all_points and (abdominal_pains_points / all_points * 100)

        return {
            "back": back_result,
            "upperBodyLimbs" : upper_body_limbs_result,
            "lowerBodyLimbs" : lower_body_limbs_result,
            "headache": headache_result,
            "abdominalPains": abdominal_pains_result
        }


class TMSNeedForInterventionView(generics.RetrieveAPIView):
    route_path = "/tms-monitoring/need-for-intervention/<int:department_id>"
    route_name = "need_for_intervention_tms"

    def get_object(self, **kwargs):
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(kwargs.get("department_id"))

        # back
        back = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.CERVICAL, constants.LUMBAR_BUTTOCKS , constants.BACK_THORAX),
            tools.IN
        )

        upper_body_limbs = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.SHOULDERS, constants.ELBOW_WIRST_HAND),
            tools.IN
        )

        lower_body_limbs = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HIP, constants.KNEES, constants.LEG_FOOT),
            tools.IN
        )

        headache = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HEADACHE,),
            tools.IN
        )

        abdominal_pains = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.ABDOMINAL_PAIN,),
            tools.IN
        )

        return {
            "back" : back,
            "upperBodyLimbs" : upper_body_limbs,
            "lowerBodyLimbs" : lower_body_limbs,
            "headache": headache,
            "abdominalPains": abdominal_pains
        }
