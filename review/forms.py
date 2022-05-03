from django import forms
from django.forms import ModelForm
from review.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            "review_text",
            "rating",
        )

    review_text = forms.CharField(
        max_length=1000, widget=forms.Textarea(attrs={"type": "text", "id": "review-text", "rows": "4"})
    )
    rating = forms.IntegerField()

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating is None:
            raise forms.ValidationError("Please rate the product before submit.")
        return rating
