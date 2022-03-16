from django.db import models
from account.models import UserBase
from store.models import Product

# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="wishlist_user")
    product = models.ManyToManyField(Product, related_name="wishlist_product")
