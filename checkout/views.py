from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
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
from django.views.generic import View, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin

# Create your views here.


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


class DeliveryAddressView(TemplateView):
    template_name = "checkout/delivery_address.html"

    def get(self, request):
        session = request.session
        if "purchase" not in request.session:
            messages.success(request, "Please select delivery option")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

        try:
            self.address = Address.objects.get(customer_id=request.user.id)

        except ObjectDoesNotExist:
            return render(request, "checkout/delivery_address.html")

        else:
            if "address" not in request.session:
                session["address"] = {"address_id": str(self.address)}
            else:
                session["address"]["address_id"] = str(self.address)
                session.modified = True
            return render(
                request,
                "checkout/delivery_address.html",
                context={
                    "address": self.address,
                },
            )


class PaymentView(View):
    def get(self, request):
        try:
            address = Address.objects.get(customer_id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, "checkout/delivery_address.html")
        else:
            return render(request, "checkout/payment_selection.html", context={"address": address})

    def post(self, request):
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
