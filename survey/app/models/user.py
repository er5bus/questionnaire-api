from .. import mongo
from ._behaviors import TimestampMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class Role:
    ADMIN = 1
    MODERATE = 2
    EMPLOYEE = 4


class User(mongo.DynamicDocument, TimestampMixin):
    username = mongo.StringField(unique=True)
    email = mongo.StringField(unique=True)
    enabled = mongo.BooleanField()
    member_since = mongo.DateTimeField(default=datetime.utcnow)
    last_seen = mongo.DateTimeField(default=datetime.utcnow)
    salt = mongo.StringField()
    hashed_password = mongo.StringField()
    confirmed = mongo.BooleanField(default=False)
    deleted_at = mongo.DateTimeField(default=None)
    roles = mongo.ListField()

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def can(self, perm):
        for role in self.roles:
            if role.has_role(perm):
                return True
        return False

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def add_role(self, perm):
        if not self.has_role(perm):
            self.roles += perm

    def remove_role(self, perm):
        if self.has_role(perm):
            self.roles -= perm

    def reset_role(self):
        if self.roles != 0:
            self.roles = 0

    def has_role(self, perm):
        return self.roles & perm == perm

