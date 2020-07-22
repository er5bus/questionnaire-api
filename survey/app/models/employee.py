from .. import mongo
from bson.objectid import ObjectId
from datetime import datetime
from .common import BaseInvitation, BaseUser


class MedicalRecord(mongo.EmbeddedDocument):
    height = mongo.StringField()
    weight = mongo.StringField()
    medical_history = mongo.StringField()
    chronic_illness = mongo.StringField()


class Employee(BaseUser, mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )

    birthday = mongo.DateTimeField()
    phone = mongo.StringField()

    medical_record = mongo.EmbeddedDocumentField(MedicalRecord, default=None)
    account = mongo.ReferenceField('app.models.account.Account')


class EmployeeInvitation(BaseInvitation, mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )

    account = mongo.EmbeddedDocumentField(Employee)

    def generate_token(self, company_id):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id), 'company_id': company_id, 'invitation': 'employee' }).decode('utf-8')
