from django.urls import path
from . import views

app_name = "basket"
urlpatterns = [
    path("", views.basket_summary, name="basket_summary"),
    path("add/", views.basket_add, name="basket_add"),
    path("delete/", views.basket_delete, name="basket_delete"),
    path("update/", views.basket_update, name="basket_update"),
    path("save_for_later/", views.basket_save_for_later, name="basket_save_for_later"),
]
