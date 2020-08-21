from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr
from .common import BaseUserSchema
from marshmallow.validate import Length


class ManagerInvitationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.ManagerInvitation
        include_relationships = False
        exclude = ("pk", "discriminator")

    subject = EscapedStr(max_length=128, required=True, validate=Length(min=1, max=500))

    token = EscapedStr(dump_only=True)
    send_at = ma.DateTime(dump_only=True)

    invitations = ma.Nested('app.schemas.common.InvitationInfoSchema', many=True)


class ManagerSchema(BaseUserSchema):
    class Meta(BaseUserSchema.Meta):
        model = models.Manager
        load_instance = True
        exclude = ("pk", "discriminator")

    company = ma.Nested('app.schemas.company.CompanySchema')
    invitation = ma.Nested(ManagerInvitationSchema)
