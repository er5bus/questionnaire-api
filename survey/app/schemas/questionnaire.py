from .. import models, ma
from .common import BaseUserSchema
from ._behaviors import BaseSchema, EscapedStr
from marshmallow.validate import Length


class QuestionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Question
        exclude = BaseSchema.Meta.exclude + ("question_type", )
        dump_only = tuple()

    name = EscapedStr(max_length=128, required=True, validate=[Length(max=255, min=1)])
    score = ma.Int(required=True)
    type = EscapedStr(max_length=128, attribute="question_type", required=True, validate=[Length(max=255, min=1)])


class QuestionnaireSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Questionnaire
        dump_only = BaseSchema.Meta.dump_only + ("date", )

    questions = ma.Nested(QuestionSchema, many=True)
    employee = ma.Nested('app.schemas.employee.EmployeeSchema', dump_only=True, only=("id", "professional_email" , "email", "first_name", "last_name"))
