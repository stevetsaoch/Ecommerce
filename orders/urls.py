from django.urls import path, include
from . import views

app_name = "orders"

urlpatterns = [
    path("add/", views.add, name="add"),
    path("order_issue/", views.order_issue, name="order_issue"),
    path("order_issue_email/", views.order_issue_email, name="order_issue_email")]
