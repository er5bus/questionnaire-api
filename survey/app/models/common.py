from .. import db
from sqlalchemy.ext.declarative import declared_attr
from ._behaviors import Base, TimestampMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class InvitationInfo(Base, TimestampMixin):

    email = db.Column(db.String(128), unique=True)
    full_name = db.Column(db.String(200))

    invitation_pk = db.Column(db.Integer, db.ForeignKey('baseinvitation.pk'))
    invitation = db.relationship('BaseInvitation', backref=db.backref("invitationList", lazy="joined"), foreign_keys=[invitation_pk])


class BaseInvitation(Base, TimestampMixin):

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = { 'polymorphic_identity': 'baseinvitation', 'polymorphic_on': discriminator }

    subject = db.Column(db.String(128))
    token = db.Column(db.Text)
    send_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_created = db.Column(db.Boolean, default=True)

    company_pk = db.Column(db.Integer, db.ForeignKey('company.pk'))
    company = db.relationship('app.models.company.Company', backref=db.backref("invitations", lazy="joined"), foreign_keys=[company_pk])

    account = db.relationship('app.models.common.BaseUser', back_populates='invitation')


class BaseUser(Base, TimestampMixin):

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = { 'polymorphic_identity': 'baseuser', 'polymorphic_on': discriminator }

    hashed_password = db.Column(db.String(128))

    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(128), unique=True)
    role = db.Column(db.Integer, nullable=True)

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    enabled = db.Column(db.Boolean, default=True)
    member_since = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    invitation_pk = db.Column(db.Integer, db.ForeignKey('baseinvitation.pk'))
    invitation = db.relationship(BaseInvitation, back_populates='account')

    company_pk = db.Column(db.Integer, db.ForeignKey('company.pk'))
    company = db.relationship('app.models.company.Company', backref=db.backref("employees", lazy="joined"), foreign_keys=[company_pk])

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, plain_password):
        self.hashed_password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.hashed_password, plain_password)

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


class Role:
    ADMIN = 1
    MODERATOR = 2
    EMPLOYEE = 4
