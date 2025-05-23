from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import random

from .forms import RegisterForm, LoginForm

User = get_user_model()

# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require activation
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, "This user name exists olease aplly a different one")
                return render(request, "users/register.html", {"form": form})
            user.save()

            # Sending Activation Email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            domain = get_current_site(request).domain
            protocol = 'https' if request.is_secure() else 'http'
            link = f"{protocol}://{domain}/users/activate/{uid}/{token}/"
            subject = "Activate your account"
            message = f"Click the link to activate your account:\n{link}"
            send_mail(subject, message, 'admin@crowdfund.com', [user.email])
            return HttpResponse("Check your email to activate your account.")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

# Account Activation View
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Account activated successfully!")
    else:
        return HttpResponse("Activation link is invalid!")

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

# redirect after login
@login_required
def home(request):
    return render(request, 'users/home.html')




