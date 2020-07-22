from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class BaseUserSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.BaseUser

    first_name = EscapedStr(max_length=150, required=True, validate=Length(max=200, min=1))
    last_name = EscapedStr(max_length=150, required=True, validate=Length(max=128, min=1))

