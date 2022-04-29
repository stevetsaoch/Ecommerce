from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from .basket import Basket
from basket.models import Basket_db
from store.models import Product
from account.models import UserBase
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class BasketView(TemplateView):
    template_name = "basket/summary.html"

    def setup(self, request, **args):
        super().setup(request, **args)
        self.basket = Basket(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["basket"] = self.basket
        return context

    def post(self, request):
        # add prodcut to basket and show the correct total number of product in basket
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        self.basket.add(product=product, qty=product_qty)
        basketqty = self.basket.__len__()
        response = JsonResponse({"qty": basketqty})
        return response

    def delete(self, request):
        product_id = int(QueryDict(request.body).get("productid"))
        self.basket.delete(product=product_id)

        basketqty = self.basket.__len__()
        baske_total_before_tax = self.basket.get_subtotal_price_before_tax()
        baskek_total_after_tax = self.basket.get_subtotal_price_after_tax()
        response = JsonResponse(
            {
                "qty": basketqty,
                "basket_total_before_tax": baske_total_before_tax,
                "basket_total_after_tax": baskek_total_after_tax,
            }
        )
        return response

    def patch(self, request):
        # update quantity of product in the basket
        product_id = int(QueryDict(request.body).get("productid"))
        post_quantity = int(QueryDict(request.body).get("post_quantity"))
        action = QueryDict(request.body).get("action")

        # get product inventory
        product_inventory = Product.objects.get(id=product_id).inventory

        if action == "increase-product-quantity":
            # check whether quantity after increasing will higher than product quantity
            if post_quantity == product_inventory:
                post_quantity = post_quantity

            elif post_quantity > product_inventory:
                post_quantity -= 1

            else:
                post_quantity = post_quantity

        if action == "decrease-product-quantity":
            # check whether quantity after decreasing will less than 1
            if post_quantity < 1:
                post_quantity += 1

            else:
                if post_quantity + 1 == product_inventory:
                    post_quantity = post_quantity

                post_quantity = post_quantity


        self.basket.update(product=product_id, qty=post_quantity)

        basketqty = self.basket.__len__()
        basket_product_subtotal = self.basket.get_product_total_before_tax(product_id)
        basket_total_before_tax = self.basket.get_subtotal_price_before_tax()
        baskek_total_after_tax = self.basket.get_subtotal_price_after_tax()
        response = JsonResponse(
            {
                "qty": basketqty,
                "product_inventory": product_inventory,
                "post_quantity": post_quantity,
                "product_total": basket_product_subtotal,
                "basket_total_before_tax": basket_total_before_tax,
                "basket_total_after_tax": baskek_total_after_tax,
            }
        )
        return response
