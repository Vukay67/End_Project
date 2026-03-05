from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AuthenticationForm, RegistrationForm

def main_page(request):
    context = {
    }
    return render(request, "index.html", context)

def about_page(request):
    return render(request, "about.html", {})

def contacts_page(request):
    return render(request, "contacts.html", {})

def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("main_page")
    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(request, "login.html", context)

def register_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = User.objects.create_user(
                email=email,
                username=username,
                password=password
            )
            login(request, user)
            return redirect("main_page")
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def profil_page(request):
    return render(request, "profil.html", {})