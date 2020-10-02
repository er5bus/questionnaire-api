from .. import ma, db
from flask import escape, Markup


class EscapedStr(ma.Field):

    def deserialize(self, value, attr=None, data = None, **kwargs):
        field_content = super().deserialize(value, attr, data, **kwargs)
        return escape(field_content) if isinstance(field_content, str) else field_content

    def serialize(self, value, *args, **kwargs):
        field_content = super().serialize(value, *args, **kwargs)
        return Markup.unescape(field_content) if field_content else None