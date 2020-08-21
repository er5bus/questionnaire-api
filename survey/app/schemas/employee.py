from .. import models, ma
from .common import BaseUserSchema
from ._behaviors import BaseSchema, EscapedStr
from marshmallow.validate import Length


class MedicalRecordSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.MedicalRecord


class EmployeeSchema(BaseUserSchema):
    class Meta(BaseUserSchema.Meta):
        model = models.Employee
        exclude = ("pk", "discriminator")

    invitation = ma.Nested("EmployeeInvitationSchema")
    medical_record = ma.Nested(MedicalRecordSchema)


class EmployeeInvitationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.EmployeeInvitation
        include_relationships = False
        exclude = ("pk", "discriminator")

    subject = EscapedStr(max_length=128, required=True, validate=Length(min=1, max=500))

    token = EscapedStr(dump_only=True)
    send_at = ma.DateTime(dump_only=True)

    invitations = ma.Nested("app.schemas.common.InvitationInfoSchema", many=True)

