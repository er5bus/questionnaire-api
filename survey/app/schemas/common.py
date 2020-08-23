from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr
from marshmallow.validate import Length, Email


class InvitationInfoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.InvitationInfo
        dump_only = tuple()

    email = EscapedStr(max_length=128, required=True, validate=[Length(max=128, min=1), Email()])
    full_name = EscapedStr(max_length=128, required=True)


class BaseInvitationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.BaseInvitation
        exclude = BaseSchema.Meta.exclude + ("discriminator", "is_expired", "token", "send_at")

    company = ma.Nested('app.schemas.company.CompanySchema')
    department = ma.Nested('app.schemas.company.DepartmentSchema')


class BaseUserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.BaseUser
        load_instance = True
        exclude = BaseSchema.Meta.exclude + ("discriminator", "hashed_password")

    email = EscapedStr(max_length=128, required=True, validate=[Length(max=128, min=1), Email()])
    professional_email = EscapedStr(max_length=128, required=True, validate=[Length(max=128, min=1), Email()])
    username = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    password = EscapedStr(max_length=128, required=True, load_only=True)
    role = ma.Int(dump_only=True)
