from .. import db
from ._mixins import Base
from datetime import datetime


class Questionnaire(Base):
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    employee_pk = db.Column(db.Integer, db.ForeignKey("baseuser.pk"), nullable=True)
    employee = db.relationship("src.models.employee.Employee", foreign_keys=[employee_pk])

    question_categories = db.relationship("QuestionCategory")


class QuestionCategory(Base):
    category = db.Column(db.String(200))
    score = db.Column(db.Integer, nullable=True)
    questions = db.relationship("Question")

    questionnaire_pk = db.Column(db.Integer, db.ForeignKey("questionnaire.pk", ondelete="CASCADE"))
    questionnaire = db.relationship("Questionnaire", back_populates="question_categories", lazy=True, foreign_keys=[questionnaire_pk])


class Question(Base):
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    area = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    category_pk = db.Column(db.Integer, db.ForeignKey("questioncategory.pk", ondelete="CASCADE"))
    category = db.relationship("QuestionCategory", back_populates="questions", lazy=True, foreign_keys=[category_pk])
