from bson.objectid import ObjectId
from .. import mongo
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

class ManagerInvitation(mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )
    email = mongo.EmailField()
    full_name = mongo.StringField()
    subject = mongo.StringField()
    token = mongo.StringField()
    send_at = mongo.DateTimeField(default=None)
    authenticated = mongo.BooleanField( default=False )

    user = mongo.ReferenceField('survey.models.user.User')

    def generate_token(self, company_id):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id), 'company_id': company_id, 'invitation': 'manager' }).decode('utf-8')


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
    manager_invitations = mongo.EmbeddedDocumentListField(ManagerInvitation, default=list)
