from .. import db
from ._mixins import Base
from datetime import datetime


class Questionnaire(Base):
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    employee_pk = db.Column(db.Integer, db.ForeignKey("baseuser.pk"), nullable=True)
    employee = db.relationship("src.models.employee.Employee", foreign_keys=[employee_pk])

    questions = db.relationship("Question")
    scores = db.relationship("Score")


class Question(Base):
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    questionnaire_pk = db.Column(db.Integer, db.ForeignKey("questionnaire.pk", ondelete="CASCADE"))
    questionnaire = db.relationship("Questionnaire", back_populates="questions", lazy=True, foreign_keys=[questionnaire_pk])


class Score(Base):
    name = db.Column(db.Text, nullable=True)
    descriptions = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    questionnaire_pk = db.Column(db.Integer, db.ForeignKey("questionnaire.pk", ondelete="CASCADE"))
    questionnaire = db.relationship("Questionnaire", back_populates="scores", lazy=True, foreign_keys=[questionnaire_pk])
