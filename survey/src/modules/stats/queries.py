from ... import models, db
from sqlalchemy import func
from .tools import escape_string


def get_all_questions_by_department(department_pk):
    rows = db.session.query(
        models.Employee.pk.label("employee"),
        models.Employee.email.label("employee_email"),
        models.QuestionCategory.category.label("category") ,
        models.QuestionCategory.score.label("category_score"),
        models.Question.question.label("question"),
        models.Question.answer.label("answer"),
        models.Question.area.label("area"),
        models.Question.score.label("area_score"),
    ).join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
        join(models.Question, models.Question.category_pk == models.QuestionCategory.pk). \
        join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
        join(models.Department, models.Department.pk == models.Employee.department_pk). \
        filter(models.Department.pk == department_pk). \
        all()

    data = []
    for row in rows:
        data.append({ "employee_id": row[0], "employee_email": row[1], "category": row[2], 
                "category_score": row[3], "question": escape_string(row[4]), 
                "answer": escape_string(row[5]), "area": escape_string(row[6]), "question_score": row[7] })
    return data



def get_all_point_by_department_group_by_category(department_pk):
    rows = db.session.query(
        func.sum(models.QuestionCategory.score).label("category_score"), 
        models.QuestionCategory.category.label("category")
    ). \
        join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
        join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
        join(models.Department, models.Department.pk == models.Employee.department_pk). \
        filter(models.Department.pk == department_pk). \
        group_by(models.QuestionCategory.category). \
        all()

    kpis = []
    for row in rows:
        kpis.append({ "category_score": row[0], "category": row[1]})
    return kpis


def get_all_employee_of_department(department_pk):
    row = db.session.query(
        func.count(models.Employee.pk).label("count_employee"),
    ). \
        join(models.Department, models.Employee.department_pk == models.Department.pk). \
        filter(models.Department.pk == department_pk). \
        scalar()

    return row

def get_all_point_by_department_group_by_category_and_employee(department_pk):
    rows = db.session.query(
        func.sum(models.QuestionCategory.score).label("category_score"),
        models.QuestionCategory.category.label("category"),
        models.Employee.pk.label("employee"),
    ). \
        join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
        join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
        join(models.Department, models.Department.pk == models.Employee.department_pk). \
        filter(models.Department.pk == department_pk). \
        group_by(models.QuestionCategory.category, models.Employee.pk). \
        all()

    kpis = []
    for row in rows:
        kpis.append({ "category_score": row[0], "category": row[1], "employee": row[2]})
    return kpis


def get_all_point_by_department_group_by_category_and_area(department_pk):
    rows = db.session.query(
        func.sum(models.QuestionCategory.score).label("category_score"),
        models.QuestionCategory.category.label("category") ,
        func.sum(models.Question.score).label("area_score"),
        models.Question.area.label("area")
    ).join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
        join(models.Question, models.Question.category_pk == models.QuestionCategory.pk). \
        join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
        join(models.Department, models.Department.pk == models.Employee.department_pk). \
        filter(models.Department.pk == department_pk). \
        group_by(models.QuestionCategory.category, models.Question.area). \
        all()

    kpis = []
    for row in rows:
        kpis.append({ "category_score": row[0], "category": row[1], "area_score": row[2], "area": row[3]})
    return kpis


def get_all_point_by_department_group_by_category_and_area_and_employee(department_pk):
    rows = db.session.query(
        func.sum(models.QuestionCategory.score).label("category_score"),
        models.QuestionCategory.category.label("category") ,
        func.sum(models.Question.score).label("area_score"),
        models.Question.area.label("area"),
        models.Employee.pk.label("employee")
    ).join(models.Questionnaire, models.Questionnaire.pk == models.QuestionCategory.questionnaire_pk). \
        join(models.Question, models.Question.category_pk == models.QuestionCategory.pk). \
        join(models.Employee, models.Employee.pk == models.Questionnaire.employee_pk). \
        join(models.Department, models.Department.pk == models.Employee.department_pk). \
        filter(models.Department.pk == department_pk). \
        group_by(models.QuestionCategory.category, models.Question.area, models.Employee.pk). \
        all()

    kpis = []
    for row in rows:
        kpis.append({ "category_score": row[0], "category": row[1], "area_score": row[2], "area": row[3], "employee": row[4]})
    return kpis
