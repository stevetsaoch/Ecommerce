from django.http import HttpResponse, QueryDict
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from .prodcuts import ProductPaginator, ProductTools

from .models import Category, Product
from account.models import UserBase
from orders.models import Order, OrderItem
from review.models import Review

from review.forms import ReviewForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class ProductAll(ListView):
    template_name = "store/index.html"
    model = Product

    def patch(self, request, *args, **kwargs):
        # plus one in product click_counter when user click
        slug = QueryDict(request.body)["slug"]
        product = get_object_or_404(Product, slug=slug, in_stock=True)
        product.click_counter += 1
        product.save()

        return HttpResponse(status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.request.GET.get("page", 1)
        # all product pagination
        all_product = Product.objects.all()
        all_product_paginated = ProductPaginator(all_product).paginate(page_num, item_per_page=10)

        # popular product pagination
        popular_product = Product.objects.all().order_by("-click_counter")
        popular_product_paginated = ProductPaginator(popular_product).paginate(page_num, item_per_page=5)

        # update context
        context["all_product_paginated"] = all_product_paginated
        context["popular_product_paginated"] = popular_product_paginated
        return context


class ProdcutSingle(DetailView):
    model = Product
    template_name = "store/single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        product = self.object
        _range = ProductTools(product).quantity_range()
        review_all = Review.objects.filter(product=product.id)
        review_form = ReviewForm()

        # check if user is logined, then return form or not
        if not self.request.user.is_authenticated:
            # if there are no reviews lefted for current prodcut
            context["prodcut"] = product
            context["range"] = _range
            context["review_all"] = review_all
        else:
            # Check wether current user had buy this product
            user_id = self.request.user.id
            # order_ids of current user
            user_order_id = Order.objects.filter(user_id=user_id)
            # all kind of product that user had buy
            user_order_items = (
                OrderItem.objects.filter(order_id__in=user_order_id).values_list("product_id", flat=True).distinct()
            )
            # Render review_form if user had buy this product
            if product.id in user_order_items:
                try:
                    current_user_left_review = Review.objects.get(reviewer=user_id, product=product.id)
                except ObjectDoesNotExist:
                    context["prodcut"] = product
                    context["range"] = _range
                    context["review_all"] = review_all
                    context["review_form"] = review_form
                else:
                    context["prodcut"] = product
                    context["range"] = _range
                    context["review_all"] = review_all
            else:
                # if user has lefted review in this prodcut, then don't show review form
                context["prodcut"] = product
                context["range"] = _range
                context["review_all"] = review_all

        return context


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/category.html", context={"category": category, "products": products})


class CategoryProductAll(ListView):
    template_name = "store/category.html"
    model = Category

    def get_queryset(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs["category_slug"])
        products = Product.objects.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.request.GET.get("page", 1)
        # Category all product pagination
        category_all_product_paginated = ProductPaginator(self.object_list).paginate(page_num, item_per_page=10)
        # update context
        context["category_all_product_paginated"] = category_all_product_paginated
        context["category"] = Category.objects.get(slug=self.kwargs["category_slug"])
        return context
