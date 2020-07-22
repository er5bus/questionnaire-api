from .. import mongo
from ._behaviors import TimestampMixin, IdMixin
from .common import BaseInvitation, BaseUser
from bson.objectid import ObjectId
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


class Moderator(BaseUser, mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )

    birthday = mongo.DateTimeField()
    phone = mongo.StringField()

    account = mongo.ReferenceField('app.models.account.Account')


class ManagerInvitation(BaseInvitation, mongo.EmbeddedDocument):

    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )
    email = mongo.EmailField()
    full_name = mongo.StringField()
    subject = mongo.StringField()
    token = mongo.StringField()
    send_at = mongo.DateTimeField(default=None)
    is_created = mongo.BooleanField( default=False )

    account = mongo.ReferenceField("app.models.account.Account", default=None)

    def generate_token(self, company_id):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': str(self.id), 'company_id': company_id, 'invitation': 'manager' }).decode('utf-8')
