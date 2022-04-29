from django.http import HttpResponse
from django.views.generic import View

# local app
from review.forms import ReviewForm
from account.models import UserBase
from store.models import Product

# Views

class ReviewView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_id = request.user.id

    def post(self, request):
        user = UserBase.objects.get(id=self.user_id)
        product = Product.objects.get(id=request.POST["productid"])
        form_input = {"rating": int(request.POST["rating"]), "review_text": request.POST["review_text"]}
        review_form = ReviewForm(form_input)
        if review_form.is_valid():
            review_form = review_form.save(commit=False)
            review_form.reviewer = user
            print("checkpoint1")
            review_form.product = product
            print("checkpoint2")
            review_form.save()
            print("checkpoint3")
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)
