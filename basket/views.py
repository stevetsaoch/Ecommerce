from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .basket import Basket
from store.models import Product


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
        response = JsonResponse({
            "qty": basketqty, 
            "basket_total_before_tax": baske_total_before_tax,
            "basket_total_after_tax": baskek_total_after_tax,
            })
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
        response = JsonResponse({
            "qty": basketqty,
            "product_total": basket_product_subtotal,
            "basket_total_before_tax": baske_total_before_tax,
            "basket_total_after_tax": baskek_total_after_tax,
            })
        return response
