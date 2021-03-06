from .. import models, ma
from .common import BaseUserSchema
from ._base import BaseSchema
from ._types import EscapedStr
from marshmallow.validate import Length, OneOf


class QuestionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Question
        dump_only = tuple()

    question = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    answer = EscapedStr(max_length=500, required=True, validate=[Length(max=500, min=1)])
    area = EscapedStr(max_length=500, required=False)
    score = ma.Int(required=False)


class QuestionCategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.QuestionCategory
        dump_only = tuple()

    category = EscapedStr(max_length=500, required=True)
    score = ma.Int(required=False)
    questions = ma.Nested(QuestionSchema, many=True, required=False)


class QuestionnaireSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Questionnaire
        dump_only = BaseSchema.Meta.dump_only + ("date", )

    question_categories = ma.Nested(QuestionCategorySchema, many=True)
    employee = ma.Nested('src.schemas.employee.EmployeeSchema', dump_only=True, only=("id", "professional_email" , "email", "first_name", "last_name"))
