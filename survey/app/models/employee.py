from .. import db
from ._behaviors import Base
from ._types import JsonEncodedDict
from .common import BaseUser, BaseInvitation
from datetime import datetime


class Employee(BaseUser):

    __mapper_args__ = {'polymorphic_identity':'employee'}
    birthday = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    #phone =db.Column(db.String(20))

    medical_record_pk = db.Column(db.Integer, db.ForeignKey('medicalrecord.pk'))
    medical_record = db.relationship('MedicalRecord', foreign_keys=[medical_record_pk])

    question_history_pk = db.Column(db.Integer, db.ForeignKey('questionhistory.pk'))
    question_history = db.relationship('QuestionHistory', foreign_keys=[medical_record_pk])


class QuestionHistory(Base):

    current_page = db.Column(db.Integer)
    selected_body_area = db.Column(JsonEncodedDict)
    current_Question = db.Column(db.Integer)
    scores = db.Column(JsonEncodedDict)
    answered_questions = db.Column(JsonEncodedDict)
    extra_args = db.Column(JsonEncodedDict)


class MedicalRecord(Base):

    sexe = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.String(50))
    tall = db.Column(db.String(50))
    profession = db.Column(db.String(200))
    home_work = db.Column(db.Integer)


class EmployeeInvitation(BaseInvitation):
    __mapper_args__ = {'polymorphic_identity':'employeeinvitation'}
