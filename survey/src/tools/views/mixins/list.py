from ._base import BaseMethodMixin


class ListMixin(BaseMethodMixin):
    """
    List model objects.
    """

    def list (self, *args, **kwargs):
        paginator = self.paginate_query(**kwargs)
        return dict(items=self.serialize(paginator.items, True), has_more=paginator.has_next, pages=paginator.pages, total=paginator.total, page=paginator.page), 200
