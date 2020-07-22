from .. import mongo
from .employee import Employee
from .moderator import Moderator, ManagerInvitation
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


class Company(mongo.Document):
    name = mongo.StringField()
    description = mongo.StringField()
    universal_name = mongo.StringField()
    company_type = mongo.StringField()
    status = mongo.StringField()
    employee_count_range = mongo.StringField()
    specialities = mongo.StringField()
    location = mongo.StringField()
    founded_year = mongo.StringField()

    author = mongo.ReferenceField('app.models.account.Account')
    manager_invitations = mongo.EmbeddedDocumentListField(ManagerInvitation, default=list)
    employees = mongo.EmbeddedDocumentListField(Employee, default=list)

