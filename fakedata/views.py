from django.shortcuts import render
from store.models import Product
# Create your views here.

print(Product.objects.all())
