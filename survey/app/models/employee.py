from .. import db
from ._behaviors import Base
from .common import BaseUser, BaseInvitation
from datetime import datetime


class Employee(BaseUser):

    __mapper_args__ = {'polymorphic_identity':'employee'}
    birthday = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    #phone =db.Column(db.String(20))

    medical_record_pk = db.Column(db.Integer, db.ForeignKey('medicalrecord.pk'))
    medical_record = db.relationship('MedicalRecord', foreign_keys=[medical_record_pk])


class MedicalRecord(Base):

    sexe = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.String(50))
    tall = db.Column(db.String(50))
    profession = db.Column(db.String(200))
    home_work = db.Column(db.Integer)


class EmployeeInvitation(BaseInvitation):
    __mapper_args__ = {'polymorphic_identity':'employeeinvitation'}

    def generate_token(self, company_id):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id), 'company_id': company_id, 'invitation': 'employee' }).decode('utf-8')
