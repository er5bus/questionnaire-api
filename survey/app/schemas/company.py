from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class CompanySchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.Company

    name = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    description = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=1))
    universal_name = EscapedStr(max_length=100, required=True, validate=Length(max=100, min=1))
    company_type = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=1))
    status = EscapedStr(max_length=50, required=True, validate=Length(max=50, min=1))
    employee_count_range = EscapedStr(max_length=20, required=True, validate=Length(max=20, min=1))
    specialities = EscapedStr(max_length=40, required=True, validate=Length(max=40, min=1))
    location = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    founded_year = EscapedStr(max_length=20, required=True)


class ManagerInvitationSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.ManagerInvitation

    email = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    full_name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=1))
    subject = EscapedStr(max_length=128, required=True, validate=Length(min=1, max=500))

    token = EscapedStr(dump_only=True)
    send_at = ma.DateTime(dump_only=True)

    is_created = ma.Boolean(dump_only=True)

