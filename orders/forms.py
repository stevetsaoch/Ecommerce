from django import forms
from orders.models import OrderIssue


class OrderIssue(forms.ModelForm):
    class Meta:
        model = OrderIssue
        fields = ("email", "content", "orderid")

    email = forms.EmailField(
        label="Your email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email"}),
    )

    content = forms.CharField(
        label="Please report your issue, we will process it as soon as possible, thanks you.",
        max_length=1000,
        widget=forms.Textarea(attrs={"class": "form-control", "id": "review-text", "rows": "4"}),
    )

    orderid = forms.CharField(
        label="Your order id",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "orderid",
                "id": "form-orderid",
                "readonly": "readonly",
            }
        ),
    )
