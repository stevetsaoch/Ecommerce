from django.db import models
from account.models import UserBase
from store.models import Product

# Create your models here.


class Review(models.Model):
    reviewer = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="review_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review_product", default=None)
    review_text = models.CharField(max_length=1000, blank=True, default="")
    rating = models.IntegerField(blank=False)
    post_time = models.DateTimeField(auto_now_add=True)