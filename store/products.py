from django.db.models import QuerySet
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from .models import Product


class ProductPaginator:
    def __init__(self, objects: QuerySet, paginator: Paginator = Paginator):
        self._objects = objects
        self._paginator = paginator

    def paginate(self, page_num: int, item_per_page: int = 5):

        paginated = self._paginator(self._objects, item_per_page)
        try:
            paginated_object = paginated.page(page_num)
        except PageNotAnInteger:
            paginated_object = paginated.page(1)
        except EmptyPage:
            paginated_object = paginated.page(paginated.num_pages)

        return paginated_object


class ProductTools:
    def __init__(self, product: Product):
        self.product = product

    def quantity_range(self):
        quantity = self.product.inventory
        if quantity == 0:
            _range = range(0, 1)
        elif quantity > 0 and quantity < 5:
            _range = range(1, self.product.inventory + 1)
        elif quantity >= 5:
            _range = range(1, 6)

        return _range