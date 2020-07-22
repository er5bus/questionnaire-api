from .. import mongo
from datetime import datetime
from bson.objectid import ObjectId


class TimestampMixin(object):
    """
    add created at and update at fields
    """
    created = mongo.DateTimeField(default=datetime.utcnow)
    updated = mongo.DateTimeField(default=datetime.utcnow)


class IdMixin(object):
    """
    add id field
    """
    id = mongo.ObjectIdField(primary_key=True, default=lambda: ObjectId() )
