from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length, Email


class InvitationInfoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.InvitationInfo


class BaseInvitationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.BaseInvitation
        include_relationships = False
        exclude = ('discriminator', )

    invitationList = ma.List(ma.Nested('InvitationInfoSchema'))


class BaseUserSchema(BaseSchema):
    class Meta:
        model = models.BaseUser
        exclude = ('discriminator', 'company', 'hashed_password')

    email = EscapedStr(max_length=128, required=True, validate=[Length(max=128, min=1), Email()])
    username = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    password = EscapedStr(attribute='_hashed_password', max_length=128, required=False, load_only=True)
    role = ma.Int()
