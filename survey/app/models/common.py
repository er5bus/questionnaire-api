from .. import mongo
from datetime import datetime
from ._behaviors import TimestampMixin, IdMixin


class BaseInvitation(TimestampMixin):

    email = mongo.EmailField()
    full_name = mongo.StringField()
    subject = mongo.StringField()
    token = mongo.StringField()
    send_at = mongo.DateTimeField(default=None)
    is_created = mongo.BooleanField( default=False )


class BaseUser(TimestampMixin):

    first_name = mongo.StringField()
    last_name = mongo.StringField()
    member_since = mongo.DateTimeField(default=datetime.utcnow)
    last_seen = mongo.DateTimeField(default=datetime.utcnow)
