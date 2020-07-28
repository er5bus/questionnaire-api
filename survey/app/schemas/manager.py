from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class ManagerInvitationSchema(BaseSchema):
    class Meta:
        model = models.ManagerInvitation
        include_relationships = False
        exclude = ('pk',)

    id = ma.Int(attribute='pk', dump_only=True)

    email = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    full_name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=1))
    subject = EscapedStr(max_length=128, required=True, validate=Length(min=1, max=500))

    token = EscapedStr(dump_only=True)
    send_at = ma.DateTime(dump_only=True)

    is_created = ma.Boolean(dump_only=True)


class ManagerSchema(BaseSchema):
    class Meta:
        model = models.Manager
        exclude = ('pk', 'discriminator', 'hashed_password')

    id = ma.Int(attribute='pk', dump_only=True)

    company = ma.Nested('app.schemas.company.CompanySchema')
    invitation = ma.Nested(ManagerInvitationSchema)
