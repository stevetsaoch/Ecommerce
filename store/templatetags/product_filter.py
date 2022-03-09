from django.template import Library

register = Library()


@register.filter(name="getbykey")
def getbykey(value, arg):
    return value[str(arg)]
