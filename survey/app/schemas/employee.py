from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class MedicalRecordSchema(BaseSchema):
    class Meta:
        model = models.MedicalRecord
        exclude = ('pk',)

    id = ma.Int(attribute='pk', dump_only=True)


class EmployeeInvitationSchema(BaseSchema):
    class Meta:
        model = models.EmployeeInvitation
        exclude = ('pk',)

    id = ma.Int(attribute='pk', dump_only=True)


class EmployeeSchema(BaseSchema):
    class Meta:
        model = models.Employee
        exclude = ('pk', 'discriminator', 'hashed_password')

    id = ma.Int(attribute='pk', dump_only=True)

    company = ma.Nested('app.schemas.company.CompanySchema')
    invitation = ma.Nested(EmployeeInvitationSchema)
    medical_record = ma.Nested(MedicalRecordSchema)
