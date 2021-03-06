from .. import db
from ._mixins import Base
from ._types import JsonEncodedDict
from .common import BaseUser, BaseInvitation
from datetime import datetime


class Employee(BaseUser):
    __mapper_args__ = {"polymorphic_identity":"employee"}

    question_history = db.Column(JsonEncodedDict)

    medical_record_pk = db.Column(db.Integer, db.ForeignKey("medicalrecord.pk"), nullable=True)
    medical_record = db.relationship("MedicalRecord", foreign_keys=[medical_record_pk])

    department_pk = db.Column(db.Integer, db.ForeignKey("department.pk"), nullable=True)
    department = db.relationship("src.models.company.Department", backref=db.backref("employees", cascade="all, delete-orphan", lazy=True), foreign_keys=[department_pk])

    questionnaires = db.relationship("src.models.questionnaire.Questionnaire")


class MedicalRecord(Base):

    sexe = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.String(50))
    tall = db.Column(db.String(50))
    profession = db.Column(db.String(200))
    home_work = db.Column(db.Integer)


class EmployeeInvitation(BaseInvitation):

    __mapper_args__ = {"polymorphic_identity":"employeeinvitation"}

    department_pk = db.Column(db.Integer, db.ForeignKey("department.pk"), nullable=True)
    department = db.relationship("src.models.company.Department", backref=db.backref("employee_invitations", lazy=True), foreign_keys=[department_pk])
