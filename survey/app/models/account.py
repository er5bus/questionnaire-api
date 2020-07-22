from .. import mongo
from .common import BaseUser
from .employee import Employee
from ._behaviors import TimestampMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Role:
    ADMIN = 1
    MODERATOR = 2
    EMPLOYEE = 4


class Account(mongo.DynamicDocument, TimestampMixin):
    username = mongo.StringField(unique=True)
    email = mongo.StringField(unique=True)
    enabled = mongo.BooleanField()
    member_since = mongo.DateTimeField(default=datetime.utcnow)
    last_seen = mongo.DateTimeField(default=datetime.utcnow)
    salt = mongo.StringField()
    hashed_password = mongo.StringField()
    confirmed = mongo.BooleanField(default=False)
    deleted_at = mongo.DateTimeField(default=None)
    role = mongo.IntField()

    company = mongo.ReferenceField('app.models.company.Company', default=None)

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def add_role(self, perm):
        if not self.has_role(perm):
            self.role += perm

    def remove_role(self, perm):
        if self.has_role(perm):
            self.role -= perm

    def reset_role(self):
        if self.role != 0:
            self.role = 0

    def has_role(self, perm):
        return self.role & perm == perm

