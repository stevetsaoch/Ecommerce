# others
from datetime import date, datetime, timezone
import pytz

# local app
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
    today = datetime.now(pytz.UTC)
    delta = today - value
    days = delta.days

    if days >= 1:
        years = days // 365
        if years >= 1:
            if years == 1:
                return f"{years} year ago".format(years)
            if years > 1:
                return f"{years} years ago".format(years)

        months = days // 30
        if months >= 1:
            if months == 1:
                return f"{months} month ago".format(months)
            if months > 1:
                return f"{months} months ago".format(months)
        else:
            if days == 1:
                return f"{days} day ago".format(days)
            if days > 1:
                return f"{days} days ago".format(days)

    if days < 1:
        hours = delta.seconds // 3600
        if hours >= 1:
            if hours == 1:
                return f"{hours} hour ago".format(hours)
            if hours > 1:
                return f"{hours} hours ago".format(hours)
        else:
            mins = (delta.seconds % 3600) // 60
            if mins <= 1:
                return f"{mins} minute ago".format(mins)
            else:
                return f"{mins} minutes ago".format(mins)


@register.filter(name="ratingaverage")
def ratingaverage(value):
    reviews = Review.objects.filter(product_id=value)
    reviews_rating = list(reviews.values_list("rating", flat=True))
    if not reviews_rating:
        return "0.0"
    else:
        reviews_rating_average = round(sum(reviews_rating) / len(reviews), 1)
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
