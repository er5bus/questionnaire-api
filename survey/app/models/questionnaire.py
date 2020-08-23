from .. import db
from ._behaviors import Base
from datetime import datetime


class Questionnaire(Base):
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    employee_pk = db.Column(db.Integer, db.ForeignKey("baseuser.pk"), nullable=True)
    employee = db.relationship("app.models.employee.Employee", foreign_keys=[employee_pk])

    questions = db.relationship("Question")


class Question(Base):
    name = db.Column(db.String(255), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    question_type = db.Column(db.String(255), nullable=True)

    questionnaire_pk = db.Column(db.Integer, db.ForeignKey("questionnaire.pk", ondelete="CASCADE"))
    questionnaire = db.relationship("Questionnaire", back_populates="questions", lazy=True, foreign_keys=[questionnaire_pk])
