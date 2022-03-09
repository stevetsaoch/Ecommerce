from store.models import Category, Product
from basket.basket import Basket


def categories(request):
    return {"categories": Category.objects.all()}


def range_dict(request):
    # contrust qty range for each product
    basket = Basket(request)
    product_ids = basket.basket.keys()
    products = Product.objects.filter(id__in=product_ids)
    range_dict = {}

    for product in products:
        if product.inventory > 5:
            range_dict[str(product.id)] = range(1, 6)
        else:
            range_dict[str(product.id)] = range(1, product.inventory + 1)
    return {"range_dict": range_dict}
