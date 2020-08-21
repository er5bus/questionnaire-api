from .. import ma, db
from ..views import utils
from flask import escape, Markup
from functools import partialmethod


class EscapedStr(ma.Field):

    def deserialize(self, value, attr = None, data = None, **kwargs):
        field_content = super().deserialize(value, attr, data, **kwargs)
        return escape(field_content) if isinstance(field_content, str) else field_content

    def serialize(self, value, *args, **kwargs):
        field_content = super().serialize(value, *args, **kwargs)
        return Markup.unescape(field_content)


class BaseSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(attribute='pk')

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = utils.camelcase(field_obj.data_key or field_name)

    class Meta:
        load_instance = True
        exclude = ("pk", )
        dump_only = ("id", )
