from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse

# django views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView

# local app
from account.account import formdata_extract
from account.models import UserBase, Address
from account.forms import RegistrationForm, UserEditForm, AddressEditForm
from account.token import account_activation_token
from basket.basket import Basket
from basket.models import Basket_db
from store.models import Product

# Views


class AccountRegisterForm(CreateView):
    template_name = "account/registration/register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.email = form.cleaned_data["email"]
        self.object.set_password(form.cleaned_data["password"])
        self.object.is_active = False
        self.object.save()
        current_site = get_current_site(self.request)
        subject = "Activate your Account"
        message = render_to_string(
            "account/registration/account_activation_email.html",
            context={
                "user": self.object,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.object.pk)),
                "token": account_activation_token.make_token(self.object),
            },
        )
        self.object.email_user(subject=subject, message=message)
        return render(self.request, "account/registration/register_email_confirm.html", context={"form": self.object})


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

            # create a address instance for user passing activation
            Address.objects.create(customer_id=user.id)
            return redirect("account:dashboard")
        else:
            return render(request, "account/registration/activation_invalid.html")


class ProfileView(TemplateView):
    template_name = "account/dashboard/profile/profile.html"

    def setup(self, request, *args, **kwargs):
        user_id = request.user.id
        self.profile = UserBase.objects.get(id=user_id)
        self.address = Address.objects.get(customer_id=user_id)
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        context["address"] = self.address

        return context


class ProfileEditView(View):
    def setup(self, request, *args, **kwargs):
        self.user = request.user
        self.user_id = request.user.id
        super().setup(request, *args, **kwargs)

    def post(self, request):
        user_data = formdata_extract(UserEditForm(), request)

        # binding profile image to user_form
        user_form = UserEditForm(data=user_data, files=request.FILES, instance=self.user)

        address_data = formdata_extract(AddressEditForm(), request)
        address_data["full_name"] = user_data["first_name"] + " " + user_data["last_name"]
        # get address instance for current user and update it
        address_data["customer"] = self.user_id
        address_instance = Address.objects.get(customer_id=self.user_id)
        address_form = AddressEditForm(data=address_data, instance=address_instance)
        # data validation and save
        if user_form.is_valid() & address_form.is_valid():
            # save user change
            user_form.save()

            # save address change
            address_form.save()
            return HttpResponseRedirect(reverse("account:profile"))

        return render(
            request,
            "account/dashboard/profile/profile_edit_details.html",
            context={"user_form": user_form, "address_form": address_form},
        )

    def get(self, request):
        user_form = UserEditForm(instance=self.user, use_required_attribute=False)
        address_form = AddressEditForm(instance=self.user, use_required_attribute=False)
        return render(
            request,
            "account/dashboard/profile/profile_edit_details.html",
            context={"user_form": user_form, "address_form": address_form},
        )

    def patch(self, request):
        user = UserBase.objects.get(id=self.user_id)
        user.is_active = False
        user.save()
        logout(request)

        return HttpResponse(status=200)


class CustomLogoutView(LogoutView):
    next_page = "/account/login/"

    # PUT data from in-session basket into Basket_db when logout
    def setup(self, request, *args, **kwargs):
        user = UserBase.objects.get(id=request.user.id, is_active=True)
        basket = request.session.get("skey")

        basket_in_db = Basket_db.objects.filter(user=user)
        if not basket_in_db:
            # Save basket to db if user didn't save any
            for key, value in basket.items():
                product = Product.objects.get(id=int(key))
                basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
                basket_db.save()
        else:
            # Add new product from in-session basket to Basket_db
            basket_in_db_list = basket_in_db.values_list("product", flat=True)
            for key, value in basket.items():
                if int(key) not in basket_in_db_list:
                    product = Product.objects.get(id=int(key))
                    basket_db = Basket_db.objects.create(user=user, product=product, quantity=int(value["qty"]))
                    basket_db.save()

            # Update basket_db
            for product in basket_in_db:
                # if prodcut is remove from in-session basket
                if str(product.product_id) not in list(basket.keys()):
                    product.delete()

                # Update product quantity if it was change
                elif str(product.product_id) in list(basket.keys()):
                    if product.quantity != basket.get(str(product.product_id))["qty"]:
                        product.quantity = basket.get(str(product.product_id))["qty"]
                        product.save()
                    else:
                        pass
        super().setup(request, *args, **kwargs)
