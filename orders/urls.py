from django.urls import path, include
from . import views
from .views import OrderView, OrderIssueView
from django.contrib.auth.decorators import login_required
from django.urls import re_path

app_name = "orders"

urlpatterns = [
    path("user_orders/", login_required(OrderView.as_view()), name="user_orders"),
    path("order_issue/<str:order_key>", login_required(OrderIssueView.as_view()), name="order_issue"),
    ]
