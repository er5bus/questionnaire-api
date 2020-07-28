from .. import db
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from datetime import datetime


class AutoTableNameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class AutoPKMixin(object):
    @declared_attr
    def pk(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = db.ForeignKey(base.pk)
                break
        else:
            type = db.Integer

        return db.Column(type, primary_key=True)

    @declared_attr
    def __tablepk__(cls):
        return "{0}.pk".format(cls.__name__.lower())


class TimestampMixin(object):
    @declared_attr
    def created(cls):
        return db.Column(db.DateTime, default=datetime.now())

    @declared_attr
    def updated(cls):
        return db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Base(db.Model, AutoTableNameMixin, AutoPKMixin):
    __abstract__ = True
