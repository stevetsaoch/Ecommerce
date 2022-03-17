from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='store_home'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/product_count', views.product_count, name='product_count'),
    path('store/<slug:category_slug>/', views.category_list, name='category_list'),
]
