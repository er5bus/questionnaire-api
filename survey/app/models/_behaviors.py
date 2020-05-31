from .. import mongo
from datetime import datetime


class TimestampMixin(object):
    """
    add created at and update at fields
    """
    created = mongo.DateTimeField(default=datetime.utcnow)
    updated = mongo.DateTimeField(default=datetime.utcnow)
