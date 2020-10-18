from .. import db
from sqlalchemy.ext.declarative import declared_attr
from ._mixins import Base, TimestampMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


class InvitationInfo(Base, TimestampMixin):

    email = db.Column(db.String(128), unique=True)
    full_name = db.Column(db.String(200), nullable=True)

    invitation_pk = db.Column(db.Integer, db.ForeignKey("baseinvitation.pk", ondelete="CASCADE"))
    invitation = db.relationship("BaseInvitation", back_populates="invitations", lazy=True, foreign_keys=[invitation_pk])


class BaseInvitation(Base, TimestampMixin):

    discriminator = db.Column("type", db.String(50))
    __mapper_args__ = { "polymorphic_identity": "baseinvitation", "polymorphic_on": discriminator }

    subject = db.Column(db.String(128))
    token = db.Column(db.Text, default=uuid.uuid4())
    send_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_expired = db.Column(db.Boolean, default=False)

    accounts = db.relationship("BaseUser", back_populates="invitation")
    invitations = db.relationship(InvitationInfo, back_populates="invitation", cascade="all, delete", passive_deletes=True, lazy=True)


class Role:
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 4


class BaseUser(Base, TimestampMixin):

    discriminator = db.Column("type", db.String(50))
    __mapper_args__ = { "polymorphic_identity": "simpleuser", "polymorphic_on": discriminator }

    hashed_password = db.Column(db.String(128))

    email = db.Column(db.String(128), unique=True)
    professional_email = db.Column(db.String(128), unique=True, nullable=True)
    username = db.Column(db.String(128), unique=True)
    role = db.Column(db.Integer, nullable=True)

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    enabled = db.Column(db.Boolean, default=True)
    member_since = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    invitation_pk = db.Column(db.Integer, db.ForeignKey("baseinvitation.pk"))
    invitation = db.relationship("BaseInvitation", back_populates="accounts")


    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    @password.setter
    def password(self, plain_password):
        self.hashed_password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.hashed_password, plain_password)

    def is_administrator(self):
        return self.can(Role.ADMIN)

    def add_role(self, role):
        if not self.has_role(role):
            self.role += role

    def remove_role(self, role):
        if self.has_role(role):
            self.role -= role

    def reset_role(self):
        if self.role != 0:
            self.role = 0

    def has_role(self, role):
        return self.role & role == role
