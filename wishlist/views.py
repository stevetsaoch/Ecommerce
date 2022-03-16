from django.http import HttpResponse
from django.shortcuts import render
from wishlist.models import WishList
from django.contrib.auth.decorators import login_required
from account.models import UserBase
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your views here.

@login_required
def user_wishlist(request):
    user_id = request.user.id
    user_wishlist = WishList.objects.get(user=user_id)
    products = user_wishlist.product.all()
    range_dict = {}
    for product in products:
        qty = product.inventory
        if qty > 0 and qty < 5:
            _range = range(1, product.inventory + 1)
            range_dict[str(product.id)] = _range
        elif qty > 5:
            _range = range(1, 6)
            range_dict[str(product.id)] = _range
    return render(request, 'account/wishlist/user_wishlist.html', context={
        'user_wishlist': user_wishlist, 'range': range_dict
    })

@login_required
def wishlist_add(request):
    if request.method == 'POST':
        user_id = request.user.id
        product_id = int(request.POST.get('productid'))

        # check if product is already in wishlist, if it does then return success
        try:
            w_list = WishList.objects.get(user=user_id)
            product = Product.objects.get(id=product_id)
            if product not in w_list.product.all():
                w_list.product.add(product)
                return HttpResponse(status=201)
            else:
                return HttpResponse(status=201)
        # if user is not setup an wish, create a wishlist and followed by adding product
        except ObjectDoesNotExist:
            user_instance = UserBase.objects.get(id=user_id)
            product_instance = Product.objects.get(id=product_id)
            w_list = WishList.objects.create(user=user_instance)
            w_list.save()
            w_list.product.add(product_instance)
            return HttpResponse(status=201)

@login_required
def wishlist_delete(request):
    product_id = int(request.POST.get("productid"))
    w_list = WishList.objects.get(user=request.user.id)
    product_instance = Product.objects.get(id=product_id)
    w_list.product.remove(product_instance)

    return HttpResponse(status=201)



