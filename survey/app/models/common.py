from .. import db
from sqlalchemy.ext.declarative import declared_attr
from ._behaviors import Base, AccountMixin, TimestampMixin
from datetime import datetime


class BaseInvitation(Base, TimestampMixin):

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = { 'polymorphic_identity': 'baseinvitation', 'polymorphic_on': discriminator }

    email = db.Column(db.String(128), unique=True)
    full_name = db.Column(db.String(200))
    subject = db.Column(db.String(128))
    token = db.Column(db.Text)
    send_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_created = db.Column(db.Boolean, default=True)

    company_pk = db.Column(db.Integer, db.ForeignKey('company.pk'))
    company = db.relationship('app.models.company.Company', backref=db.backref("invitations", lazy="joined"), foreign_keys=[company_pk])

    account = db.relationship('app.models.common.BaseUser', back_populates='invitation')


class BaseUser(Base, AccountMixin, TimestampMixin):

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = { 'polymorphic_identity': 'baseuser', 'polymorphic_on': discriminator }

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


class Role:
    ADMIN = 1
    MODERATOR = 2
    EMPLOYEE = 4
