from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('user_wishlist/', views.user_wishlist, name='user_wishlist'),
    path('wishlist_add', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete', views.wishlist_delete, name='wishlist_delete'),
]