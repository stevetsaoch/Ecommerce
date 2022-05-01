from django.urls import include, path
from . import views
from .views import DeliveryOptionView, PaymentView
from django.contrib.auth.decorators import login_required

app_name = "checkout"

urlpatterns = [
    path("deliveryoptions/", login_required(DeliveryOptionView.as_view()), name="delivery_options"),
    path("payment/", login_required(PaymentView.as_view()), name="payment"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]
