from http import HTTPStatus
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm
from account.models import UserBase
from store.models import Product
# Create your views here.

@login_required
def review_add(request):
    user = UserBase.objects.get(id=request.user.id)
    product = Product.objects.get(id=request.POST["productid"])
    form_input = {
        "rating": int(request.POST["rating"]),
        "review_text": request.POST["review_text"]
    }
    if request.method == 'POST':
        review_form = ReviewForm(form_input)
        if review_form.is_valid():
            review_form = review_form.save(commit=False)
            review_form.reviewer = user
            review_form.product = product
            review_form.save()
    return HttpResponse(status=200)
