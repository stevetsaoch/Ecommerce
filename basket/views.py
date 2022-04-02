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
        action = request.POST.get("action")
        if action == "add-product-to-basket":
            # add prodcut to basket and show the correct total number of product in basket
            product_id = int(request.POST.get("productid"))
            product_qty = int(request.POST.get("productqty"))
            product = get_object_or_404(Product, id=product_id)
            self.basket.add(product=product, qty=product_qty)
            basketqty = self.basket.__len__()
            response = JsonResponse({"qty": basketqty})

            return response

        elif action == "save-session-basket-to-basket-db":
            if self.request.user.is_authenticated:
            # check if user already have basket saved in db
                user = UserBase.objects.get(id=request.user.id)
                basket = request.session.get("skey")
                basket_in_db = Basket_db.objects.filter(user=user)

                if not basket_in_db:
                    # Save basket to db if user didn't save any
                    for key, value in basket.items():
                        product = Product.objects.get(id=int(key))
                        basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
                        basket_db.save()
                else:
                    # Add new product from in-session basket to Basket_db
                    basket_in_db_list = basket_in_db.values_list("product", flat=True)
                    for key, value in basket.items():
                        if int(key) not in basket_in_db_list:
                            product = Product.objects.get(id=int(key))
                            basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
                            basket_db.save()

                    # Update basket_db
                    for product in basket_in_db:
                        # if prodcut is remove from in-session basket
                        if str(product.product_id) not in list(basket.keys()):
                            product.delete()

                        # Update product quantity if it was change
                        elif str(product.product_id) in list(basket.keys()):
                            if product.quantity != basket.get(str(product.product_id))["qty"]:
                                product.quantity = basket.get(str(product.product_id))["qty"]
                                product.save()
                            else:
                                pass

                # Reload basket to session if user logout and login again
                return HttpResponse(status=201)

            else:
                return HttpResponseForbidden("Please login!")

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
        product_qty = int(QueryDict(request.body).get("productqty"))
        self.basket.update(product=product_id, qty=product_qty)

        basketqty = self.basket.__len__()
        basket_product_subtotal = self.basket.get_product_total_before_tax(product_id)
        basket_total_before_tax = self.basket.get_subtotal_price_before_tax()
        baskek_total_after_tax = self.basket.get_subtotal_price_after_tax()
        response = JsonResponse(
            {
                "qty": basketqty,
                "product_total": basket_product_subtotal,
                "basket_total_before_tax": basket_total_before_tax,
                "basket_total_after_tax": baskek_total_after_tax,
            }
        )
        return response


@login_required
def basket_save_for_later(request):
    # check if user already have basket saved in db
    user = UserBase.objects.get(id=request.user.id)
    basket = request.session.get("skey")

    basket_in_db = Basket_db.objects.filter(user=user)
    if not basket_in_db:
        # Save basket to db if user didn't save any
        for key, value in basket.items():
            product = Product.objects.get(id=int(key))
            basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
            basket_db.save()
    else:
        # Add new product from in-session basket to Basket_db
        basket_in_db_list = basket_in_db.values_list("product", flat=True)
        for key, value in basket.items():
            if int(key) not in basket_in_db_list:
                product = Product.objects.get(id=int(key))
                basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
                basket_db.save()

        # Update basket_db
        for product in basket_in_db:
            # if prodcut is remove from in-session basket
            if str(product.product_id) not in list(basket.keys()):
                product.delete()

            # Update product quantity if it was change
            elif str(product.product_id) in list(basket.keys()):
                if product.quantity != basket.get(str(product.product_id))["qty"]:
                    product.quantity = basket.get(str(product.product_id))["qty"]
                    product.save()
                else:
                    pass

    # Reload basket to session if user logout and login again
    return HttpResponse(status=200)
