from ._base import BaseMethodMixin
from collections import Iterable


class RetrieveMixin(BaseMethodMixin):
    """
    Retrieve a model instance
    """

    def retrieve (self, *args, **kwargs):
        instance = self.get_object(**kwargs)
        return self.serialize(instance, False), 200
