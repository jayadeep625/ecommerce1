from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfileForm
from orders.models import Order
from wishlist.models import Wishlist

def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    return render(request, "home.html")

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

    else:

        form = ProfileForm(instance=profile)

    context = {

        "profile": profile,

        "form": form,

        "total_orders": Order.objects.filter(
            user=request.user
        ).count(),

        "wishlist_count": Wishlist.objects.filter(
            user=request.user
        ).count(),

    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )

