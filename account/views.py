from distutils.log import error
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from account.models import UserBase, Address
from .forms import RegistrationForm, UserEditForm, AddressEditForm
from django.template.loader import render_to_string
from .token import account_activation_token
from orders.views import user_orders
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django import forms

# Create your views here.


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})


@login_required
def dashboard(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/dashboard.html", {"orders": orders})


@login_required
def profile(request):
    profile = UserBase.objects.get(id=request.user.id)
    try:
        address = Address.objects.get(customer_id=request.user.id)
    except ObjectDoesNotExist:
        return render(
            request,
            "account/dashboard/profile.html",
            context={
                "profile": profile,
            },
        )

    return render(
        request,
        "account/dashboard/profile.html",
        context={
            "profile": profile,
            "address": address,
        },
    )


def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            # if .save(commit=False) is called by a model form, it will return a model instance.
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                context={
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_email_confirm.html", context={"form": registerForm})

    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", context={"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    else:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("account:dashboard")
        else:
            return render(request, "account/registration/activation_invalid.html")


@login_required
def edit_details(request):
    print(request.META["HTTP_REFERER"])
    if request.method == "POST":
        user_data = formdata_extract(UserEditForm(), request)

        # binding profile image to user_form
        user_form = UserEditForm(data=user_data, files=request.FILES, instance=request.user)
        address_data = formdata_extract(AddressEditForm(), request)
        address_data["full_name"] = user_data["first_name"] + " " + user_data["last_name"]
        # get address instance for current user
        try:
            address_instance = Address.objects.get(customer_id=request.user.id)

        # add address if there is no address for current user
        except ObjectDoesNotExist:
            address_data["customer"] = request.user.id
            address_form = AddressEditForm(data=address_data)
        else:
            address_data["customer"] = request.user.id
            address_form = AddressEditForm(instance=address_instance, data=address_data)

        # data validation and save
        if user_form.is_valid() & address_form.is_valid():
            # save user change
            user_form.save()

            # save address change
            address_form.save()
            
            if "delivery_address" in request.META["HTTP_REFERER"]:
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
            else:
                return HttpResponseRedirect(reverse("account:profile"))
    else:
        user_form = UserEditForm(instance=request.user, use_required_attribute=False)
        address_form = AddressEditForm(instance=request.user, use_required_attribute=False)
    return render(
        request, "account/dashboard/edit_details.html", context={"user_form": user_form, "address_form": address_form}
    )


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


# Addresses


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please choice a delivery option.")


##
def formdata_extract(form, request_data):
    dict = {}
    fields = form.Meta.fields
    for field in fields:
        if isinstance(form.fields[field], forms.ImageField) or isinstance(form.fields[field], forms.FileField):
            pass
        else:
            if field == "customer" or field == "full_name":
                dict[field] = ""
            else:
                dict[field] = request_data.POST[field]
    return dict
