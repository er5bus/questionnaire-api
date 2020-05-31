from ._base import BaseMethodMixin
from flask import request


class CreateMixin(BaseMethodMixin):
    """
    Create a model instance
    """
    def create (self, *args, **kwargs):
        instance = self.deserialize(request.json)
        self.perform_create(instance)
        return self.serialize(instance), 201

    def perform_create(self, instance):
        instance.save()
