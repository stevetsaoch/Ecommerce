import json

# django
from django.http import HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, ListView, TemplateView

# local app
from checkout.models import DeliveryOptions, PaymentSelections
from basket.basket import Basket
from account.models import Address
from orders.models import Order, OrderItem
from store.models import Product

# paypal
from checkout.paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest

# Views


class DeliveryOptionView(ListView):
    model = DeliveryOptions
    template_name = "checkout/delivery_choices.html"

    def get_context_object_name(self, object_list):
        return "delivery_options"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deliveryoptions"] = DeliveryOptions.objects.filter(is_active=True)
        return context

    def put(self, request):
        # Update delivery options
        basket = Basket(request)
        delivery_option = int(QueryDict(request.body)["deliveryoption"])
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


# class DeliveryAddressView(View):
    
#     def get(self, request):
#         session = request.session
#         if "purchase" not in request.session:
#             messages.success(request, "Please select delivery option")
#             return HttpResponseRedirect(request.META["HTTP_REFERER"])

#         try:
#             self.address = Address.objects.get(customer_id=request.user.id)

#         except ObjectDoesNotExist:
#             return render(request, "checkout/delivery_address.html")

#         else:
#             if "address" not in request.session:
#                 session["address"] = {"address_id": str(self.address)}
#             else:
#                 session["address"]["address_id"] = str(self.address)
#                 session.modified = True
#             return render(
#                 request,
#                 "checkout/delivery_address.html",
#                 context={
#                     "address": self.address,
#                 },
#             )

class PaymentView(View):

    def get(self, request):

        session = request.session
        address = Address.objects.get(customer_id=request.user.id)
        if "purchase" not in request.session:
            messages.success(request, "Please select delivery option")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

        else:
            if "address" not in request.session:
                session["address"] = {"address_id": str(address)}
            else:
                session["address"]["address_id"] = str(address)
                session.modified = True

        return render(request, "checkout/payment_selection.html", context={"address": address})

    def post(self, request):
        user_id = request.user.id
        body = json.loads(request.body)
        # get payment source
        payment_source = body["paymentSource"]
        payment_instance = PaymentSelections.objects.get(name=payment_source)

        # send a request to paypal to fetch order information
        PPClient = PayPalClient()
        data = body["orderID"]
        requestorder = OrdersGetRequest(data)
        response = PPClient.client.execute(requestorder)

        # basket instance
        basket = Basket(request)

        # address instance
        address_instance = Address.objects.get(customer_id=user_id)

        # delivery option instance
        delivery_id = request.session["purchase"]["delivery_id"]
        delivery_instance = DeliveryOptions.objects.get(id=int(delivery_id))

        order = Order.objects.create(
            user_id=user_id,
            address=address_instance,
            payment_option=payment_instance,
            delivery_option=delivery_instance,
            email=response.result.payer.email_address,
            total_paid=response.result.purchase_units[0].amount.value,
            order_key=response.result.id,
            billing_status=True,
        )

        # save order item
        for item in basket:
            OrderItem.objects.create(order=order, product=item["product"], quantity=item["qty"])

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
