from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .basket import Basket
from basket.models import Basket_db
from store.models import Product
from account.models import UserBase
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def basket_summary(request):
    basket = Basket(request)
    return render(
        request,
        "basket/summary.html",
        context={
            "basket": basket,
        },
    )


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({"qty": basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baske_total_before_tax = basket.get_subtotal_price_before_tax()
        baskek_total_after_tax = basket.get_subtotal_price_after_tax()
        response = JsonResponse(
            {
                "qty": basketqty,
                "basket_total_before_tax": baske_total_before_tax,
                "basket_total_after_tax": baskek_total_after_tax,
            }
        )
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        basket_product_subtotal = basket.get_product_total_before_tax(product_id)
        baske_total_before_tax = basket.get_subtotal_price_before_tax()
        baskek_total_after_tax = basket.get_subtotal_price_after_tax()
        response = JsonResponse(
            {
                "qty": basketqty,
                "product_total": basket_product_subtotal,
                "basket_total_before_tax": baske_total_before_tax,
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
        for item in basket_in_db:
            # if prodcut is remove from in-session basket
            if str(item.product_id) not in list(basket.keys()):
                item.delete()
            
            # Update product quantity if it was change
            elif str(item.product_id) in list(basket.keys()):
                if item.quantity != basket.get(str(item.product_id))["qty"]:
                    item.quantity = basket.get(str(item.product_id))["qty"]
                    item.save()
                else:
                    pass

    # Reload basket to session if user logout and login again
    return HttpResponse(status=200)
