from .. import mongo
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    author = mongo.ReferenceField('survey.models.user.User')


class CompanyInvitation(mongo.DynamicDocument):
    email = mongo.EmailField()
    name = mongo.StringField()
    subject = mongo.StringField()
    token = mongo.StringField(unique=True)
    expired_at = mongo.DateTimeField(default=datetime.utcnow)

    author = mongo.ReferenceField('survey.models.user.User')

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        self.token = s.dumps({ 'email': self.email }).decode('utf-8')

