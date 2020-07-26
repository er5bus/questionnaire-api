from .. import db
from ._behaviors import Base
from .common import BaseUser, BaseInvitation
from datetime import datetime


class Employee(BaseUser):

    __mapper_args__ = {'polymorphic_identity':'employee'}
    birthday = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    #phone =db.Column(db.String(20))


class MedicalRecord(Base):
    height = db.Column(db.String(200))
    weight = db.Column(db.String(200))
    medical_history = db.Column(db.String(200))
    chronic_illness = db.Column(db.String(200))

    #employee_pk = db.Column(db.Integer, db.ForeignKey('employee.pk'))
    #employee = db.relationship(Employee, backref='medical_record', foreign_keys=[employee_pk])


class EmployeeInvitation(BaseInvitation):
    __mapper_args__ = {'polymorphic_identity':'employeeinvitation'}

    def generate_token(self, company_id):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id), 'company_id': company_id, 'invitation': 'employee' }).decode('utf-8')
