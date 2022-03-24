from django.http import HttpResponse
from django.shortcuts import render
from .models import Order, OrderItem
from account.models import UserBase
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from basket.basket import Basket
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from orders.forms import OrderIssue

# Create your views here.


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        user_id = request.user.id
        order_key = request.POST.get("order_key")
        baskettotal = basket.get_total_price

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item["prodcut"], price=item["price"])
        response = JsonResponse({"success": "Return something"})
        return response


@login_required
def order_issue(request):
    if request.method == "POST":
        return HttpResponse(status=200)
    if request.method == "GET":
        orderid = request.GET.get("orderid")
        order = Order.objects.get(id=orderid)
        order_issue_form = OrderIssue(order)
        return render(
            request,
            "account/order_issue.html",
            context={
                "order_issue_form": order_issue_form,
                "order": order,
            },
        )


@login_required
def order_issue_email(request):
    if request.method == "POST":
        order = Order.objects.get(id=int(request.POST.get("orderid")))
        order_issue_form = OrderIssue(order, request.POST)

        if order_issue_form.is_valid():
            email = order_issue_form.cleaned_data["email"]
            order_id = order_issue_form.cleaned_data["orderid"]
            user = UserBase.objects.get(email=email)
            current_site = get_current_site(request)
            subject = "Order Issue, order key: {orderkey}".format(orderkey=order_id)
            message = render_to_string(
                "account/order_issue_email.html",
                context={
                    "user": user,
                    "order_id": order_id,
                    "site_name": current_site,
                },
            )
            user.email_user(subject=subject, message=message)

            return render(
                request,
                "account/order_issue_email.html",
                context={
                    "user": user,
                    "order_id": order_id,
                    "order": order,
                    "site_name": current_site,
                },
            )

