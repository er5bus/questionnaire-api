from .. import db
from ._behaviors import Base
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


class Company(Base):
    name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    universal_name = db.Column(db.String(150), nullable=True)
    company_type = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    employee_count_range = db.Column(db.String(100), nullable=True)
    specialities = db.Column(db.String(150), nullable=True)
    location = db.Column(db.Text, nullable=True)
    founded_year = db.Column(db.String(150), nullable=True)

    author_pk = db.Column(db.Integer, db.ForeignKey("baseuser.pk"))
    author = db.relationship("app.models.common.BaseUser", foreign_keys=[author_pk])


class Department(Base):
    name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)

    company_pk = db.Column(db.Integer, db.ForeignKey("company.pk"))
    company = db.relationship(Company, backref=db.backref("departments", lazy="joined"), foreign_keys=[company_pk])
