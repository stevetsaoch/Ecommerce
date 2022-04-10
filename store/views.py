from django.http import HttpResponse, QueryDict
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

# local app
from store.products import ProductPaginator, ProductTools
from store.models import Category, Product
from orders.models import Order, OrderItem
from review.models import Review
from review.forms import ReviewForm

# Views


class ProductAll(ListView):
    template_name = "store/index.html"
    model = Product

    def patch(self, request):
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
        popular_product = Product.objects.all().order_by("-click_counter")[:5]
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
        # preparing extra context data
        product = self.object
        _range = ProductTools(product).quantity_range()
        review_all = Review.objects.filter(product=product.id)
        review_form = ReviewForm()
        context = {**context, **{"product": product, "range": _range, "review_all": review_all}}
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
                context["review_form"] = review_form
            else:
                context = context

        else:
            # if user has lefted review in this product, then don't show review form
            context = context

        return context


class CategoryProductView(ListView):
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
