from ._base import BaseMethodMixin
from copy import deepcopy
from flask import request


class UpdateMixin(BaseMethodMixin):
    """
    Update model instance
    """
    def update (self, *args, **kwargs):
        instance = self.get_object(**kwargs)
        instance_updated = self.deserialize(request.json, instance, partial=True)
        self.perform_update(instance_updated, instance)

        return self.serialize(instance_updated), 200

    def partial_update (self, *args, **kwargs):
        instance = self.get_object(**kwargs)
        instance_updated = self.deserialize(request.json, instance_object=instance ,partial=True)
        self.perform_update(instance_updated, instance)

        return self.serialize(instance_updated), 200

    def perform_update(self, instance, old_instance):
        instance.save()
