from .. import models, ma
from .common import BaseUserSchema
from ._base import BaseSchema
from ._types import EscapedStr
from marshmallow.validate import Length


class QuestionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Question
        dump_only = tuple()

    question = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    answer = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    score = ma.Int(required=False)


class ScoreSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Score
        dump_only = tuple()

    name = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    descriptions = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    score = ma.Int(required=False)


class QuestionnaireSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Questionnaire
        dump_only = BaseSchema.Meta.dump_only + ("date", )

    questions = ma.Nested(QuestionSchema, many=True)
    scores = ma.Nested(ScoreSchema, many=True)
    employee = ma.Nested('src.schemas.employee.EmployeeSchema', dump_only=True, only=("id", "professional_email" , "email", "first_name", "last_name"))
