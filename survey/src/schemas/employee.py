from .. import models, ma
from .common import BaseUserSchema
from ._base import BaseSchema
from ._types import EscapedStr
from marshmallow.validate import Length


class MedicalRecordSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.MedicalRecord


class EmployeeSchema(BaseUserSchema):
    class Meta(BaseUserSchema.Meta):
        model = models.Employee

    invitation = ma.Nested("EmployeeInvitationSchema", dump_only=True)
    medical_record = ma.Nested(MedicalRecordSchema, dump_only=True)


class EmployeeInvitationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.EmployeeInvitation
        exclude = BaseSchema.Meta.exclude + ("discriminator", )

    subject = EscapedStr(max_length=128, required=True, validate=Length(min=1, max=500))

    token = EscapedStr(dump_only=True)
    send_at = ma.DateTime(dump_only=True)

    invitations = ma.Nested("src.schemas.common.InvitationInfoSchema", many=True)

