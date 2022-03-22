from django.template import Library

register = Library()


@register.filter(name="getbykey")
def getbykey(value, arg):
    return value[str(arg)]


@register.filter(name="times")
def times(value):
    return range(int(value))
