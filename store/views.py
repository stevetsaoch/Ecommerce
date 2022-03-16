from django.shortcuts import get_object_or_404, render
from .models import Category, Product

# Create your views here.


def product_all(request):
    products = Product.products.all()
    return render(request, "store/index.html", context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    qty = product.inventory
    if qty > 0 and qty < 5:
        _range = range(1, product.inventory + 1)
    elif qty > 5:
        _range = range(1, 6)
    return render(
        request,
        "store/single.html",
        context={"product": product, "range": _range},
    )


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/category.html", context={"category": category, "products": products})
