from flask import request, abort, jsonify
from ...helpers import camelcase
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_current_user
from collections import Iterable
import functools


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

    model_pk_attr = "pk"

    unique_fields = tuple()

    methods = set()

    item_per_page = 10

    def get_query(self, model_class=None, **kwargs):
        if kwargs:
            query = self.model_class.query if not model_class else model_class.query
            for field, value in kwargs.items():
                query = query.filter(getattr(self.model_class, field) == value)
            return query
        return self.model_class.query

    def get_object_query(self, **kwargs):
        if self.lookup_field_and_url_kwarg:
            filter_kwargs = self.lookup_fields(**kwargs)
            return self.get_query(**{**filter_kwargs})
        return self.get_query(**kwargs)

    def lookup_fields(self, **kwargs):
        filter_kwargs = dict()
        if kwargs:
            for lookup_field, value in kwargs.items():
                if lookup_field in self.lookup_field_and_url_kwarg:
                    filter_kwargs[self.lookup_field_and_url_kwarg[lookup_field]] = value
        return filter_kwargs

    def get_object(self, **kwargs):
        instance = self.get_object_query(**kwargs).one_or_none()
        if instance is None:
            abort(404)
        return instance

    def paginate_query(self, **kwargs):
        page = request.args.get('page', type=int, default=1)
        item_per_page = request.args.get(camelcase('item_per_page'), type=int, default=self.item_per_page)
        paginator = self.get_object_query(**kwargs).paginate(page, item_per_page, error_out=False)
        return paginator

    def filter_unique_object(self, model_class=None, **kwargs):
        model_class = self.model_class if not model_class else model_class
        return model_class.query.filter_by(**kwargs).first()

    def serialize(self, data=[], many=False, schema_class=None):
        if not schema_class and not self.schema_class:
            return data
        serializer = self.schema_class(many=many) if not schema_class else schema_class(many=many)
        return serializer.dump(data)

    def validate_unique(self, instance):
        errors = {}
        for unique_field in self.unique_fields:
            print(unique_field)
            # get object with the same field
            unique_field_value = getattr(instance, unique_field)
            unique_object = self.filter_unique_object(**{ unique_field: unique_field_value })
            # fetch the real object
            current_object = None
            if hasattr(instance, self.model_pk_attr) and getattr(instance, self.model_pk_attr):
                current_object = self.filter_unique_object(**{ self.model_pk_attr: getattr(instance, self.model_pk_attr) })
            # check if the object already exist
            if (unique_object and (not current_object or not hasattr(current_object, self.model_pk_attr))) \
                    or (unique_object and current_object and hasattr(current_object, self.model_pk_attr) 
                        and hasattr(unique_object, self.model_pk_attr) and \
                        getattr(unique_object, self.model_pk_attr) != getattr(current_object, self.model_pk_attr)):
                errors[camelcase(unique_field)] = "This field is already exist."
        if errors:
            raise ValidationError(errors)

    def deserialize(self, data=[], instance_object = None, partial=False, schema_class=None):
        try:
            serializer = self.schema_class() if not schema_class else schema_class()
            if instance_object:
                instance = serializer.load(data, unknown="EXCLUDE", instance=instance_object, partial=partial)
            else:
                instance = serializer.load(data, unknown="EXCLUDE", partial=partial)
            self.validate_unique(instance)
            return instance
        except ValidationError as err:
            self.raise_exception(err)

    def raise_exception(self, errors):
        abort(400, errors.messages)

