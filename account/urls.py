from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.urls import path
from . import views
from .views import CustomLogoutView, AccountRegisterForm, ProfileView, ProfileEditView
from orders.views import OrderView
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm
from django.contrib.auth.decorators import login_required
app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logout/", CustomLogoutView.as_view(next_page="/account/login/"), name="logout"),
    path("register/", AccountRegisterForm.as_view(), name="register"),
    path("activate/<slug:uidb64>/<slug:token>", views.account_activate, name="activate"),
    # Password reset
    # send email to your mailbox
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_comfirm/",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset/password_reset_email_comfirm/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
    ),
    # bring you to page for reset email
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url="/account/password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset/reset_status.html",
        ),
    ),
    # User profile
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path("profile/edit/", login_required(ProfileEditView.as_view()), name="edit_details"),
    path("profile/delete_user/", login_required(ProfileEditView.as_view()), name="delete_user"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(template_name="account/dashboard/profile/profile_delete_confirmation.html"),
        name="delete_confirmation",
    ),
]
