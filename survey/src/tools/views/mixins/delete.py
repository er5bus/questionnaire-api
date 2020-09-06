from ._base import BaseMethodMixin
from .... import db
from flask import Response


class DeleteMinxin(BaseMethodMixin):
    """
    Delete model instance
    """
    def destroy (self, *args, **kwargs):
        object_query = self.get_object_query(**kwargs)
        self.perform_delete(object_query)

        return Response(status=204)

    def perform_delete(self, object_query):
        object_query.delete()
        db.session.commit()

