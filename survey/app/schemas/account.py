from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length
from ._common import BaseUserSchema 


class AccountSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.Account

    full_name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=1))
    email = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    username = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    password = EscapedStr(max_length=128, required=False, load_only=True)
    role = ma.Int()

    company = ma.Nested("app.schemas.company.CompanySchema", dump_only=True)
    #user = ma.Nested(BaseUserSchema, dump_only=True)
