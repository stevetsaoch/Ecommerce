from django.urls import path, include
from . import views

app_name = "orders"

urlpatterns = [
    path("add/", views.add, name="add"),
]
