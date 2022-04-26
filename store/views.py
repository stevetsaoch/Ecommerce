import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

# local app
from store.products import ProductPaginator, random_background_image, ProductTools
from store.models import Category, Product, Promotion
from review.models import Review
from review.forms import ReviewForm
from orders.models import Order
from orders.models import OrderItem

# templatetag function
from store.templatetags.product_filter import ratingaverage, ratingaverage_fill

# Views


class ProductAll(ListView):
    template_name = "store/index.html"
    model = Product

    def get(self, request, *args, **kwargs):
        # override get
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, "exists"):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        # get context data
        context = self.get_context_data()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            response = {"product_inf": {}, "pages": context["num_pages"]}
            for product in context["all_product_paginated"].object_list:
                product_dict = {}
                product_dict["slug"] = product.slug
                product_dict["url"] = product.get_absolute_url()
                product_dict["image_url"] = product.image.image.url
                product_dict["title"] = product.title
                product_dict["authors"] = list(product.author.all().values_list("full_name", flat=True))
                product_dict["price"] = product.price
                product_dict["rating"] = str(ratingaverage(product.id))
                product_dict["rating_transfer"] = ratingaverage_fill(product.id)
                response["product_inf"][product.id] = product_dict
            return JsonResponse(response)

        return self.render_to_response(context)

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
        all_product = Product.objects.all().order_by("id")

        # all product
        all_product_paginated = ProductPaginator(all_product).paginate(page_num, item_per_page=6)
        context["num_pages"] = all_product_paginated["num_pages"]
        context["all_product_paginated"] = all_product_paginated["paginated_object"]

        # popular product in index
        popular_product = Product.objects.all().order_by("-click_counter")[:5]
        context["popular_product"] = popular_product

        # category list
        context["categories"] = Category.objects.all()

        # promotion
        context["promotions"] = Promotion.objects.all()

        return context


class CategoryProductView(ListView):
    template_name = "store/category.html"
    model = Category

    def get(self, request, *args, **kwargs):
        # override get
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, "exists"):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        # get context data
        context = self.get_context_data()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            response = {"product_inf": {}, "pages": context["num_pages"]}
            for product in context["category_all_product_paginated"].object_list:
                product_dict = {}
                product_dict["slug"] = product.slug
                product_dict["url"] = product.get_absolute_url()
                product_dict["image_url"] = product.image.image.url
                product_dict["title"] = product.title
                product_dict["authors"] = list(product.author.all().values_list("full_name", flat=True))
                product_dict["price"] = product.price
                product_dict["rating"] = str(ratingaverage(product.id))
                product_dict["rating_transfer"] = ratingaverage_fill(product.id)
                response["product_inf"][product.id] = product_dict
            return JsonResponse(response)

        return self.render_to_response(context)

    def get_queryset(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs["category_slug"])
        products = Product.objects.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.request.GET.get("page", 1)
        # Category all product pagination
        category_all_product_paginated = ProductPaginator(self.object_list).paginate(page_num, item_per_page=6)
        context["num_pages"] = category_all_product_paginated["num_pages"]
        context["category_all_product_paginated"] = category_all_product_paginated["paginated_object"]

        # category name and all category list
        context["category"] = Category.objects.get(slug=self.kwargs["category_slug"])
        context["categories"] = Category.objects.all()
        context["category_background"] = random_background_image()

        # popular product
        popular_product = Product.objects.all().order_by("-click_counter")[:5]
        context["popular_product"] = popular_product
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
