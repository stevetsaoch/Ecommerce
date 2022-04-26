# others
import os
import random

# django
from django.db.models import QuerySet
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger

# local app
from .models import Product


class ProductPaginator:
    def __init__(self, objects: QuerySet, paginator: Paginator = Paginator):
        self._objects = objects
        self._paginator = paginator
        self.num_pages = None

    def paginate(self, page_num: int, item_per_page: int = 5):

        paginated = self._paginator(self._objects, item_per_page)
        num_pages = paginated.num_pages
        try:
            paginated_object = paginated.page(page_num)
        except PageNotAnInteger:
            paginated_object = paginated.page(1)
        except EmptyPage:
            paginated_object = paginated.page(paginated.num_pages)

        return {"paginated_object": paginated_object, "num_pages": num_pages}


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


def random_background_image():
    image_list = os.listdir("static/store/images/")
    random_choose_image = random.choice(image_list)
    return "store/images/" + random_choose_image
