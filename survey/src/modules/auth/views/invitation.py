from .... import models, schemas
from ....tools.views import generics


class InvitationView(generics.RetrieveAPIView):
    route_path = "/auth/invitation/<string:token>"
    route_name = "invitation"

    model_class = models.BaseInvitation
    schema_class = schemas.BaseInvitationSchema

    lookup_field_and_url_kwarg = {"token": "token"}

    def get_object(self, **kwargs):
        return super().get_object(**kwargs, is_expired=False)

