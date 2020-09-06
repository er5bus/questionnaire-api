from .. import db
from ._mixins import Base
from .common import BaseInvitation, BaseUser
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


class Manager(BaseUser):
    __mapper_args__ = {"polymorphic_identity":"manager"}

    company_pk = db.Column(db.Integer, db.ForeignKey("company.pk"))
    company = db.relationship("src.models.company.Company", backref=db.backref("managers", lazy=True), foreign_keys=[company_pk])


class ManagerInvitation(BaseInvitation):
    __mapper_args__ = {"polymorphic_identity":"managerinvitation"}

    company_pk = db.Column(db.Integer, db.ForeignKey("company.pk"), nullable=True)
    company = db.relationship("src.models.company.Company", backref=db.backref("manager_invitations", lazy=True), foreign_keys=[company_pk])
