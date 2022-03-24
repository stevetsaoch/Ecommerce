from django import forms
from account.models import UserBase

from orders.models import Order


class OrderIssue(forms.Form):
    def __init__(self, order: Order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order
        self.user = UserBase.objects.get(id=order.user_id)
        self.fields["email"].initial = self.user.email
        self.fields["orderid"].initial = self.order.id

    email = forms.EmailField(
        label="Your email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )

    content = forms.CharField(
        label="Please report your issue, we will process it as soon as possible, thanks you.",
        max_length=1000,
        widget=forms.Textarea(attrs={"class": "form-control", "id": "review-text", "rows": "4"}),
    )

    orderid = forms.CharField(
        label="Your order id.",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "orderid", "id": "form-orderid", "readonly": "readonly"}),
    )
