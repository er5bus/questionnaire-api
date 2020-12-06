from .... import models, schemas
from ....tools.views import generics
from flask import abort, request
from flask import Response
from flask_jwt_extended import jwt_required, get_current_user


class QuestionHistoryCreateRetrieveView(generics.CreateRetrieveAPIView):

    route_path = "/question-history"
    route_name = "create-question-history"

    decorators = [ jwt_required ]

    def retrieve(self, **kwargs):
        current_user = get_current_user()
        if not hasattr(current_user, "question_history"):
            return Response(status=204)
        return current_user.question_history

    def create(self, *args, **kwargs):
        current_user = get_current_user()
        current_user.question_history = request.json
        super().perform_create(current_user)
        return current_user.question_history
