from flask import Markup


IN = 2
NOT_IN = 1

EQUAL = 0
GREATER_THAN = 1
LESS_THAN = 2


PREVENTIVE = "preventive"
MODERATE = "moderate"
IMPORTANT = "important"
URGENT = "urgent"

def escape_string(string):
    return Markup.unescape(string) if isinstance(string, str) else string


def compare_number(op, value, other_value):
    if op == EQUAL:
        return value == other_value
    elif op == GREATER_THAN:
        return value < other_value
    elif op == LESS_THAN:
        return value > other_value
    return False


def get_sum_by_category(kpis, categories, condition):
    sum_kpis = 0
    for kpis_row in kpis:
        if condition == IN:
            sum_kpis += kpis_row["category_score"] if kpis_row["category"] in categories else 0
        elif condition == NOT_IN:
            sum_kpis += kpis_row["category_score"] if kpis_row["category"] not in categories else 0
    return sum_kpis


def get_sum_by_category_and_employee_where_score(kpis, categories, condition, op, score):
    sum_kpis = 0
    for kpis_row in kpis:
        if condition == IN:
            sum_kpis += 1 if kpis_row["category"] in categories and compare_number(op, kpis_row["category_score"], score) else 0
        elif condition == NOT_IN:
            sum_kpis += 1 if kpis_row["category"] not in categories and compare_number(op, kpis_row["category_score"], score) else 0
    return sum_kpis


def get_sum_by_category_and_area(kpis, categories, areas, condition):
    sum_kpis = 0
    for kpis_row in kpis:
        if condition == IN:
            #sum_kpis += kpis_row["area_score"] if kpis_row["category"] in categories and kpis_row["area"] in areas else 0
            sum_kpis += kpis_row["area_score"] if kpis_row["area"] in areas else 0
        elif condition == NOT_IN:
            #sum_kpis += kpis_row["area_score"] if kpis_row["category"] not in categories and kpis_row["area"] not in areas else 0
            sum_kpis += kpis_row["area_score"] if kpis_row["area"] not in areas else 0
    return sum_kpis


def get_recurrence_area_by_employee(kpis, categories, areas, condition):

    recurrence = {
        PREVENTIVE: 0,
        MODERATE: 0,
        IMPORTANT: 0,
        URGENT: 0
    }
    
    for kpis_row in kpis:
        #if kpis_row["area_score"] == 1 and kpis_row["category"] in categories and kpis_row["area"] in areas:
        if kpis_row["area_score"] == 1 and kpis_row["area"] in areas:
            recurrence[PREVENTIVE] += 1
        #elif kpis_row["area_score"] == 2 and kpis_row["category"] in categories and kpis_row["area"] in areas:
        elif kpis_row["area_score"] == 2 and kpis_row["area"] in areas:
            recurrence[MODERATE] += 1
        #elif kpis_row["area_score"] == 3 and kpis_row["category"] in categories and kpis_row["area"] in areas:
        elif kpis_row["area_score"] == 3 and kpis_row["area"] in areas:
            recurrence[IMPORTANT] += 1
        #elif kpis_row["area_score"] >= 4 and kpis_row["category"] in categories and kpis_row["area"] in areas:
        elif kpis_row["area_score"] >= 4 and kpis_row["area"] in areas:
            recurrence[URGENT] += 1
    return recurrence


def get_recurrence_category_by_employee(kpis, categories, condition):

    recurrence = {
        PREVENTIVE: 0,
        MODERATE: 0,
        IMPORTANT: 0,
        URGENT: 0
    }

    for kpis_row in kpis:
        if kpis_row["category_score"] == 1 and kpis_row["category"] in categories:
            recurrence[PREVENTIVE] += 1
        elif kpis_row["category_score"] == 2 and kpis_row["category"] in categories:
            recurrence[MODERATE] += 1
        elif kpis_row["category_score"] == 3 and kpis_row["category"] in categories:
            recurrence[IMPORTANT] += 1
        elif kpis_row["category_score"] >= 4 and kpis_row["category"] in categories:
            recurrence[URGENT] += 1
    return recurrence


