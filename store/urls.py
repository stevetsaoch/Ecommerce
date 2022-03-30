from django.urls import path
from . import views
from .views import ProductAll, ProdcutSingle, CategoryProductAll

app_name = 'store'

urlpatterns = [
    path('', ProductAll.as_view(), name='store_home'),
    path('product/<slug:slug>', ProdcutSingle.as_view(), name='product_detail'),
    path('store/<slug:category_slug>/', CategoryProductAll.as_view(), name='category_list'),
]
