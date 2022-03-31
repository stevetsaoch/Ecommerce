from store.models import Category, Product
from basket.basket import Basket


def categories(request):
    return {"categories": Category.objects.all()}
