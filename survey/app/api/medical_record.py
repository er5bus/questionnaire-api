from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import abort
from flask_jwt_extended import jwt_required, get_current_user


class MedicalRecordCreateRetrieveView(generics.CreateRetrieveAPIView):

    route_path = "/medical-record"
    route_name = "create-medical-record"

    model_class = models.MedicalRecord
    schema_class = schemas.MedicalRecordSchema

    decorators = [ jwt_required ]

    def get_object():
        current_user = get_current_user()
        if not hasattr(current_user, medical_record):
            abort(401)
        return current_user.medical_record

    def perform_create(self, medical_record):
        current_user = get_current_user()
        current_user.medical_record = medical_record
        super().perform_create(medical_record)


utils.add_url_rule(api, MedicalRecordCreateRetrieveView)
