from django.http import HttpResponse, QueryDict
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

# local app
from wishlist.models import WishList
from store.models import Product

# Views


class WishListView(ListView):
    template_name = "account/wishlist/user_wishlist.html"
    model = WishList
    context_object_name = "user_wishlist"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_id = request.user.id

    def get_queryset(self):
        try:
            user_wishlist = WishList.objects.get(user_id=self.user_id)
        except ObjectDoesNotExist:
            product_in_user_wishlist = None
        else:
            product_in_user_wishlist = user_wishlist.product.all()

        return product_in_user_wishlist

    def put(self, request):
        product_id = int(QueryDict(request.body)["productid"])

        # update wishlist if it exist
        try:
            user_wishlist = WishList.objects.get(user=self.user_id)
            product = Product.objects.get(id=product_id)
            if product not in user_wishlist.product.all():
                user_wishlist.product.add(product)
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        # if user is not setup an wish, create a wishlist and followed by adding product
        except ObjectDoesNotExist:
            product = Product.objects.get(id=product_id)
            user_wishlist = WishList.objects.create(user_id=self.user_id)
            user_wishlist.save()
            user_wishlist.product.add(product)
            return HttpResponse(status=200)

    def delete(self, request):
        user_id = request.user.id
        product_id = int(QueryDict(request.body)["productid"])
        user_wishlist = WishList.objects.get(user=user_id)
        product = Product.objects.get(id=product_id)
        user_wishlist.product.remove(product)

        return HttpResponse(status=202)
