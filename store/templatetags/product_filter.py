# others
from datetime import date, datetime

from django.template import Library
from review.models import Review

register = Library()


@register.filter(name="getbykey")
def getbykey(value, arg):
    return value[str(arg)]


@register.filter(name="inttopercent")
def inttopercent(value):
    value = int(value) * 20
    return str(value)


@register.filter(name="daymonthyears")
def daymonthyears(value):
    today = datetime.now()
    # delta = today - value
    print(type(value.tzinfo))
    print(value)
    print(type(today.tzinfo))
    print(today)


@register.filter(name="ratingaverage")
def ratingaverage(value):
    reviews = Review.objects.filter(product_id=value)
    reviews_rating = list(reviews.values_list("rating", flat=True))
    if not reviews_rating:
        return "0.0"
    else:
        reviews_rating_average = round(sum(reviews_rating) / len(reviews), 2)
        return reviews_rating_average


@register.filter(name="ratingaverage_fill")
def ratingaverage_fill(value):
    reviews = Review.objects.filter(product_id=value)
    reviews_rating = list(reviews.values_list("rating", flat=True))
    if not reviews_rating:
        return "0"
    else:
        reviews_rating_average = round(sum(reviews_rating) / len(reviews), 2)
        reviews_rating_average_transfer = str(reviews_rating_average * 20)
        return reviews_rating_average_transfer
