from django.urls import path
from . import views
from .views import WishListView
from django.contrib.auth.decorators import login_required

app_name = 'wishlist'

urlpatterns = [
    path('user_wishlist/', login_required(WishListView.as_view()), name='user_wishlist'),
]