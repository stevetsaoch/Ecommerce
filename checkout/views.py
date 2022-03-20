from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import DeliveryOptions
from basket.basket import Basket
from account.models import Address
from orders.models import Order, OrderItem
from store.models import Product
from paypalcheckoutsdk.orders import OrdersGetRequest
from checkout.paypal import PayPalClient
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", context={"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {"delivery_id": delivery_type.id}
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse(
            {
                "total": updated_total_price,
                "delivery_price": delivery_type.delivery_price,
            }
        )
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    try:
        address = Address.objects.get(customer_id=request.user.id)

    except ObjectDoesNotExist:
        return render(request, "checkout/delivery_address.html")

    else:
        if "address" not in request.session:
            session["address"] = {"address_id": str(address)}
        else:
            session["address"]["address_id"] = str(address)
            session.modified = True

        return render(
            request,
            "checkout/delivery_address.html",
            context={
                "address": address,
            },
        )


@login_required
def payment_selection(request):
    try:
        address = Address.objects.get(customer_id=request.user.id)
    except ObjectDoesNotExist:
        return render(request, "checkout/delivery_address.html")
    else:
        return render(request, "checkout/payment_selection.html", context={"address": address})


###
# paypal
###


@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.address_line_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment complete!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    # update inventory
    product_ids = basket.basket.keys()
    products = Product.objects.filter(id__in=product_ids)
    for product in products:
        product.inventory -= basket.basket[str(product.id)]["qty"]
        product.save()

    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
