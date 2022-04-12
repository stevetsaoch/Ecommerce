from django.db import models
from django.conf import settings
from store.models import Product
from account.models import Address
from checkout.models import DeliveryOptions, PaymentSelections

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="order_address")
    delivery_option = models.ForeignKey(DeliveryOptions, on_delete=models.CASCADE, related_name="order_deliveryoption")
    payment_option = models.ForeignKey(PaymentSelections, on_delete=models.CASCADE, related_name="order_paymentoption")
    email = models.EmailField(max_length=254, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class OrderIssue(models.Model):
    order = models.ForeignKey(Order, related_name="order_issue_id", on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, default="", blank=True)
