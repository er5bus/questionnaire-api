from .... import models, schemas, db
from ....tools.views import generics
from flask_jwt_extended import jwt_required, get_current_user


class QuestionnairePercentageView(generics.RetrieveAPIView):

    route_path = "/questionnaires/<int:department_id>/percentage"
    route_name = "questionnaires_list_percentage"

    model_class = models.Questionnaire

    lookup_field_and_url_kwarg = {"department_id": "department_pk"}

    decorators = [ jwt_required ]

    def get_object(self, **kwargs):
        return super().get_object_query(**kwargs).count()

    def deserialize(self, data, instance_object=None, partial=False, schema_class=None):
        return {"results": data} 
