from .basket import Basket
from store.models import Product


def basket(request):
    return {"basket": Basket(request)}


def basket_range_dict(request):
    # contrust qty range for each product in basket
    basket = Basket(request)
    product_ids = basket.basket.keys()
    products = Product.objects.filter(id__in=product_ids)
    range_dict = {}

    for product in products:
        if product.inventory > 5:
            range_dict[str(product.id)] = range(1, 6)
        else:
            range_dict[str(product.id)] = range(1, product.inventory + 1)
    return {"basket_range_dict": range_dict}
