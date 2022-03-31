from django.urls import path
from . import views
from .views import ReviewView
from django.contrib.auth.decorators import login_required

app_name = "review"

urlpatterns = [
    path("", login_required(ReviewView.as_view()), name="review"),
]
