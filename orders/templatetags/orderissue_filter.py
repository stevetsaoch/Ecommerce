from django.template import Library
from orders.models import Order, OrderIssue
register = Library()

@register.filter(name="orderissueexist")
def orderissueexist(value):
    order_id = value.id
    order_issue_list = OrderIssue.objects.filter(order_id=order_id).values_list("order_id", flat=True)
    if order_id in order_issue_list:
        return True
    else:
        return False