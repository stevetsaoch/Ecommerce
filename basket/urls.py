from django.urls import path
from . import views
from .views import BasketView
app_name = "basket"
urlpatterns = [
    path("", BasketView.as_view(), name="basket"),
    # path("update/", views.basket_update, name="basket_update"),
    # path("save_for_later/", views.basket_save_for_later, name="basket_save_for_later"),
]
