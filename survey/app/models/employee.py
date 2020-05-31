from .. import mongo
from datetime import datetime


class Employee(mongo.EmbeddedDocument):
    first_name = mongo.StringField()
    last_name = mongo.StringField()
    birthday = mongo.DateTimeField()
    phone = mongo.StringField()
    member_since = mongo.DateTimeField(default=datetime.utcnow)
    last_seen = mongo.DateTimeField(default=datetime.utcnow)
    deleted_at = mongo.DateTimeField(default=None)

    author = mongo.ReferenceField('survey.models.user.User')
