from django.http import HttpResponse
from django.shortcuts import render, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm
from django.template.loader import render_to_string
from .token import account_activation_token
# Create your views here.


def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            # if .save(commit=False) is called by a model form, it will return a model instance.
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activate_email.html', context={
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            # return HttpResponse('registered succesfully and activation sent')

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', context={
        'form': registerForm
        })
