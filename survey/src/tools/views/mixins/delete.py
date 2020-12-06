from ._base import BaseMethodMixin
from .... import db
from flask import Response


class DeleteMinxin(BaseMethodMixin):
    """
    Delete model instance
    """
    def destroy (self, *args, **kwargs):
        instance = self.get_object(**kwargs)
        self.perform_delete(instance)

        return Response(status=204)

    def perform_delete(self, instance):
        db.session.delete(instance)
        db.session.commit()

