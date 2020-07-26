from .. import ma
from ..views import utils
from flask import escape
from marshmallow import pre_load, post_load, post_dump
from collections import Iterable
from functools import partialmethod


class UniqueIdMixin(object):
    id = ma.String(allow_none=True, dump_only=True)


class TimestampMixin(object):
    created = ma.DateTime()
    updated = ma.DateTime()


class EscapedStr(ma.Field):

    def deserialize(self, value, attr = None, data = None, **kwargs):
        field_content = super().deserialize(value, attr, data, **kwargs)
        return escape(field_content) if isinstance(field_content, str) else field_content


class BaseSchema(ma.ModelSchema):

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = utils.camelcase(field_obj.data_key or field_name)
