from .... import models, schemas, db
from ....tools.views import generics
from .. import constants, tools, queries


class TMSDetailsOfTroublesView(generics.RetrieveAPIView):

    route_path = "/tms-monitoring/details-of-troubles/<int:department_id>"
    route_name = "details_of_troubles_tms"

    fake_back_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_upper_body_limbs_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_lower_body_limbs_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_headache_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
    fake_abdominal_pains_data = { 20: 10, 21: 10, 22: 60, 23: 5 }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        category_and_area_kpis = queries.get_all_point_by_department_group_by_category_and_area(department_id)
        category_kpis = queries.get_all_point_by_department_group_by_category(department_id)

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

        if department_id in self.fake_back_data:
            back_result = self.fake_back_data[department_id]

        if department_id in self.fake_upper_body_limbs_data:
            upper_body_limbs_result = self.fake_upper_body_limbs_data[department_id]

        if department_id in self.fake_lower_body_limbs_data:
            lower_body_limbs_result = self.fake_lower_body_limbs_data[department_id]

        if department_id in self.fake_headache_data:
            headache_result = self.fake_headache_data[department_id]

        if department_id in self.fake_abdominal_pains_data:
            abdominal_pains_result = self.fake_abdominal_pains_data[department_id]

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

    fake_back_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }
    fake_upper_body_limbs_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }
    fake_lower_body_limbs_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }
    fake_headache_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }
    fake_abdominal_pains_data = {
        20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
        23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    }

    def get_object(self, **kwargs):
        department_id = kwargs.get("department_id")
        kpis = queries.get_all_point_by_department_group_by_category_and_area_and_employee(department_id)

        # back
        back_result = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.CERVICAL, constants.LUMBAR_BUTTOCKS , constants.BACK_THORAX),
            tools.IN
        )

        upper_body_limbs_result = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.SHOULDERS, constants.ELBOW_WIRST_HAND),
            tools.IN
        )

        lower_body_limbs_result = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HIP, constants.KNEES, constants.LEG_FOOT),
            tools.IN
        )

        headache_result = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.HEADACHE,),
            tools.IN
        )

        abdominal_pains_result = tools.get_recurrence_area_by_employee(
            kpis,
            (constants.PHYSIOTHERAPY, constants.OSTEOPATHY),
            (constants.ABDOMINAL_PAIN,),
            tools.IN
        )

        if department_id in self.fake_back_data:
            back_result =  self.fake_back_data[department_id]

        if department_id in self.fake_upper_body_limbs_data:
            upper_body_limbs_result = self.fake_upper_body_limbs_data[department_id]

        if department_id in self.fake_lower_body_limbs_data:
            lower_body_limbs_result = self.fake_lower_body_limbs_data[department_id]

        if department_id in self.fake_headache_data:
            headache_result = self.fake_headache_data[department_id]

        if department_id in self.fake_abdominal_pains_data:
            abdominal_pains_result = self.fake_abdominal_pains_data[department_id]

        return {
            "back" : back_result,
            "upperBodyLimbs" : upper_body_limbs_result,
            "lowerBodyLimbs" : lower_body_limbs_result,
            "headache": headache_result,
            "abdominalPains": abdominal_pains_result
        }
