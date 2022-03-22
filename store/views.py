from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from account.models import UserBase
from review.models import Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from review.forms import ReviewForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def product_all(request):
    # get all product
    products = Product.products.all()
    all_page_num = request.GET.get("page", 1)
    all_paginator = Paginator(products, 10)
    try:
        all_page_object = all_paginator.page(all_page_num)
    except PageNotAnInteger:
        all_page_object = all_paginator.page(1)
    except EmptyPage:
        all_page_object = all_paginator.page(all_paginator.num_pages)

    finally:
        # get popular product
        popular_products = Product.objects.all().order_by("-click_counter")[:5]
        popular_page_num = request.GET.get("page", 1)
        popular_paginator = Paginator(popular_products, 5)

        try:
            popular_page_object = popular_paginator.page(popular_page_num)
        except PageNotAnInteger:
            popular_page_object = popular_paginator.page(1)
        except EmptyPage:
            popular_page_object = popular_paginator.page(popular_paginator.num_pages)

    return render(
        request,
        "store/index.html",
        context={
            "all_product_page": all_page_object,
            "popular_product_page": popular_page_object,
        },
    )


def product_count(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    # recording click
    click = request.POST.get("click")
    product.click_counter += int(click)
    product.save()

    return HttpResponse(status=200)


def product_detail(request, slug):
    # get product detail and quantity range
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    qty = product.inventory
    _range = range(0, 1)
    if qty > 0 and qty < 5:
        _range = range(1, product.inventory + 1)
    elif qty >= 5:
        _range = range(1, 6)
    review_form = ReviewForm()

    # check if there are reviews lefted for current product
    try:
        review_all = Review.objects.filter(product=product.id)
    # if there are no reviews lefted for current prodcut
    except ObjectDoesNotExist:
        # check if user is login, then show form for entering review
        if not request.user.is_authenticated:
            return render(
                request,
                "store/single.html",
                context={"product": product, "range": _range},
            )
        else:
            return render(
                request,
                "store/single.html",
                context={
                    "product": product,
                    "range": _range,
                    "review_form": review_form,
                },
            )
    else:
        # check if user is logined, then return form or not
        if not request.user.is_authenticated:
            return render(
                request,
                "store/single.html",
                context={"product": product, "range": _range, "review_all": review_all},
            )
        # if user has lefted review in this prodcut, then don't show review form
        else:
            
            try:
                review_of_current_user = Review.objects.get(reviewer=request.user.id, product=product.id)
            except ObjectDoesNotExist:
                return render(
                    request,
                    "store/single.html",
                    context={
                        "product": product,
                        "range": _range,
                        "review_form": review_form,
                        "review_all": review_all,
                    },
                )

            else:
                return render(
                    request,
                    "store/single.html",
                    context={
                        "product": product,
                        "range": _range,
                        "review_all": review_all,
                        "review_of_current_user": review_of_current_user,
                    },
                )


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/category.html", context={"category": category, "products": products})
