from .. import ma, db
from ..tools.helpers import camelcase
from functools import partialmethod


class BaseSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(attribute='pk')

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    class Meta:
        load_instance = True
        exclude = ("pk", )
        dump_only = ("id", )
