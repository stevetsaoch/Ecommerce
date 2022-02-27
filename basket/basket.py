from itertools import product
from checkout.models import DeliveryOptions
from store.models import Product
from decimal import *
from django.conf import settings

class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overided, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session["skey"] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = product.id

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {
                "price": str(product.price),
                "qty": int(qty),
            }
        self.session.modified = True

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]

        self.session.modified = True

    def update(self, product, qty):
        """
        Update item qty in session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty

        self.session.modified = True

    def __len__(self):
        """
        get basket data and count the qty items.
        """
        return sum(item["qty"] for item in self.basket.values())

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def clear(self):
        del self.session['skey']
        del self.session['address']
        del self.session['purchase']
        self.session.modified = True
