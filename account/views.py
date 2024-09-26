from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, UserCreateForm
from .models import User


def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "user create successfully you may login now")
            return redirect("account:login")
    else:
        form = UserCreateForm()
    return render(request, "accounts/register.html", {"form": form })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("shop:home")
            form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("account:login")
