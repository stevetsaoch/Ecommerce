from re import L
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import UserBase, Address
from django_countries import widgets, countries


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(label="Enter Username", min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        max_length=100, help_text="Required", error_messages={"required": "Sorry, you will need an email"}
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat Password"})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Username", "id": "login-username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password", "id": "login-pwd"})
    )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = (
            "profile_img",
            "email",
            "user_name",
            "first_name",
            "last_name",
            "about",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    profile_img = forms.ImageField(
        label="Upload your profile picture!",
        allow_empty_file=True,
    )

    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )
    user_name = forms.CharField(
        label="Username",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Username",
                "id": "form-firstname",
                "readonly": "readonly",
            }
        ),
    )
    first_name = forms.CharField(
        label="First name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "First name",
                "id": "form-firstname",
            }
        ),
    )

    last_name = forms.CharField(
        label="Last name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Last name",
                "id": "form-firstname",
            }
        ),
    )

    about = forms.CharField(
        label="About you",
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Something about you",
                "id": "form-firstname",
            }
        ),
    )


class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "customer",
            "full_name",
            "phone",
            "country",
            "town_city",
            "postcode",
            "address_line",
            "address_line2",
        )
    
    full_name = forms.CharField(
        label="Full name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "First name",
                "id": "form-firstname",
            }
        ),
    )

    phone = forms.CharField(
        label="Phone",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Phone number",
                "id": "form-firstname",
            }
        ),
    )

    country = forms.ChoiceField(
        label="Country",
        widget=widgets.CountrySelectWidget(
            attrs={
                "class": "form-control mb-3",
                "id": "form-firstname",
            }
        ),
        choices=countries,
    )

    town_city = forms.CharField(
        label="Town & City",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Town & City",
                "id": "form-firstname",
            }
        ),
    )

    postcode = forms.CharField(
        label="Postcode",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Postcode",
                "id": "form-firstname",
            }
        ),
    )

    address_line = forms.CharField(
        label="Address line 1",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Address line 1",
                "id": "form-firstname",
            }
        ),
    )

    address_line2 = forms.CharField(
        label="Address line 2",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Address line 2",
                "id": "form-firstname",
            }
        ),
    )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError("Email address was not correct, please check again")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-newpass"}
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-new-pass2"}
        ),
    )
