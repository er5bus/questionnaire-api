from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length, Email


class BaseInvitationSchema(BaseSchema):
    class Meta:
        model = models.BaseInvitation
        include_relationships = False
        exclude = ('pk', 'discriminator')

    id = ma.Int(attribute='pk', dump_only=True)


class BaseUserSchema(BaseSchema):
    class Meta:
        model = models.BaseUser
        exclude = ('pk', 'discriminator', 'company', 'hashed_password')

    id = ma.Int(attribute='pk', dump_only=True)
    email = EscapedStr(max_length=128, required=True, validate=[Length(max=128, min=1), Email()])
    username = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    password = EscapedStr(attribute='_hashed_password', max_length=128, required=False, load_only=True)
    role = ma.Int()
