from flask import request, abort, jsonify
from ..utils import camelcase
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_current_user
from collections import Iterable
from bson.objectid import ObjectId


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
        try:
            filter_kwargs = self.lookup_fields(**kwargs)
            print(filter_kwargs)
            return model_class.objects(**filter_kwargs).get()
        except Exception:
            return None
        return None

    def lookup_fields(self, **kwargs):
        if kwargs:
            filter_kwargs = dict()
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(self.lookup_field_and_url_kwarg[lookup_field])] = value
            return filter_kwargs
        return {}

    def filter_objects(self, model_class=None, start=None, offset=None, **kwargs):
        objects = self.model_class.objects if not model_class else model_class.objects
        if kwargs:
            filter_kwargs = self.lookup_fields(**kwargs)
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(lookup_field)] = value
            return objects(**filter_kwargs)[start:offset]
        return objects[start:offset]

    def filter_unique_object(self, model_class=None, **kwargs):
        return self.filter_object(model_class=model_class, **kwargs)

    def get_object(self, model_class=None, **kwargs):
        instance = self.filter_object(model_class=model_class, **kwargs)
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
            if (unique_object and (not current_object or not hasattr(current_object, 'id'))) \
                or (unique_object and hasattr(current_object, 'id') and current_object and \
                    ObjectId.is_valid(unique_object.id) and ObjectId.is_valid(current_object.id) and \
                    str(unique_object.id) != str(current_object.id)):
                errors[camelcase(unique_field)] = "This field is already exist."
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
