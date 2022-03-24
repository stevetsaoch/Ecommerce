from django.db import models
from store.models import Product
from account.models import UserBase

# Create your models here.

class Basket_db(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_product")
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="basket_user")
    quantity = models.IntegerField(default=0)
