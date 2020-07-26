from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class MedicalRecordSchema(BaseSchema):
    class Meta:
        model = models.MedicalRecord

    height = EscapedStr(max_length=150, required=True, validate=Length(max=200, min=1))
    weight = EscapedStr(max_length=150, required=True, validate=Length(max=128, min=1))
    medical_history = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    chronic_illness = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))


class EmployeeSchema(BaseSchema):
    class Meta:
        model = models.Employee

    first_name = EscapedStr(max_length=150, required=True, validate=Length(max=200, min=1))
    last_name = EscapedStr(max_length=150, required=True, validate=Length(max=128, min=1))
    phone = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))

    # Change me later
    password = EscapedStr(max_length=150, required=True, validate=Length(max=128, min=1))
    username = EscapedStr(max_length=128, required=True, validate=Length(max=128, min=1))
    email = EscapedStr(max_length=128, required=True, validate=Length(max=500, min=1))
