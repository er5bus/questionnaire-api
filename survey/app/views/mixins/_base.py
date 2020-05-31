from flask import request, abort, jsonify
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_current_user
from collections import Iterable


class BaseMethodMixin:
    """
    Base API methods
    """

    route_path = None
    route_name = None

    model_class = None
    schema_class = None

    # lookup_field as the key and lookup_url_kwarg as the value
    lookup_field_and_url_kwarg = dict()

    unique_fields = tuple()

    methods = set()

    item_per_page = 10

    def filter_object(self, model_class=None, **kwargs):
        model_class = self.model_class if not model_class else model_class
        if kwargs:
            filter_kwargs = dict()
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(lookup_field)] = value
            try:
                return model_class.objects(**filter_kwargs).get()
            except model_class.DoesNotExist:
                return None
        return None

    def filter_objects(self, model_class=None, start=None, offset=None, **kwargs):
        objects = self.model_class.objects if not model_class else model_class.objects
        if kwargs:
            filter_kwargs = dict()
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(lookup_field)] = value
            return objects(**filter_kwargs)[start:offset]
        return objects[start:offset]

    def filter_unique_object(self, model_class=None, **kwargs):
        return self.filter_object(model_class=model_class, **kwargs)

    def get_object(self, model_class=None, **kwargs):
        filter_kwargs = {}
        for lookup_field, lookup_url_kwarg in self.lookup_field_and_url_kwarg.items():
            filter_kwargs[lookup_field] = kwargs.get(lookup_url_kwarg, None)
        instance = self.filter_object(model_class=model_class, **filter_kwargs)
        if instance is None:
            abort(404)
        return instance

    def paginate_objects(self, model_class=None, **kwargs):
        page = request.args.get("page", type=int, default=1)
        item_per_page = request.args.get("item_per_page", type=int, default=self.item_per_page)
        offset = (page * item_per_page)
        start = (offset - item_per_page)
        items = self.filter_objects(model_class=model_class, start=start, offset=offset, **kwargs)
        return items, len(items) == item_per_page, page

    def serialize(self, data = [], many=False, schema_class=None):
        serializer = self.schema_class(many=many) if not schema_class else schema_class(many=many)
        return serializer.dump(data)

    def validate_unique(self, instance, current_object = None):
        errors = {}
        for unique_field in self.unique_fields:
            unique_object = self.filter_unique_object(**{ unique_field: getattr(instance, unique_field) })
            if (unique_object and (not current_object or not hasattr(current_object, 'id'))) or (unique_object and hasattr(current_object, 'id') and current_object and str(unique_object.id) != str(current_object.id)):
                errors[unique_field] = "This {} is already exist.".format(unique_object.__class__.__name__)
        if errors:
            raise ValidationError(errors)

    def deserialize(self, data = [], instance_object = None, partial=False, schema_class=None):
        try:
            serializer = self.schema_class() if not schema_class else schema_class()
            serializer.context = dict(instance=instance_object)
            instance = serializer.load(data, unknown="EXCLUDE", partial=partial)
            self.validate_unique(instance, instance_object)
            return instance
        except ValidationError as err:
            self.raise_exception(err)

    def raise_exception(self, errors):
        abort(400, errors.messages)
