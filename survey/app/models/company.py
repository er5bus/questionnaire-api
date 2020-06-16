from bson.objectid import ObjectId
from .. import mongo
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class ManagerInvitation(mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )
    email = mongo.EmailField()
    name = mongo.StringField()
    subject = mongo.StringField()
    token = mongo.StringField()
    send_at = mongo.DateTimeField(default=datetime.utcnow)

    def __init__(self, *args, **kwargs ) :
        super().__init__(*args, **kwargs)
        self.token = self.generate_token()

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id) }).decode('utf-8')


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
