from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AuthenticationForm, RegistrationForm
from .models import *
from django.db import models as db_models
from django.shortcuts import get_object_or_404
from random import choices

def main_page(request):
    anime = Anime.objects.prefetch_related('genres').all()
    ran_ani = choices(anime)

    context = {
        "anime": anime,
        "ran_ani": ran_ani
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

@login_required
def profil_page(request):
    return render(request, "profil.html", {})

def anime_detail_page(request, slug):
    anime = get_object_or_404(
        Anime.objects.prefetch_related('genres', 'seasons__episodes'),
        slug=slug
    )
    context = {
        "anime": anime,
    }

    return render(request, "anime_detail.html", context)

def all_anime_page(request):
    search_query = request.GET.get('search', '')
    genre_id = request.GET.get('genres', '')
    sort_option = request.GET.get('sort', '')

    animes = Anime.objects.prefetch_related('genres', 'seasons__episodes')

    if search_query:
        animes = animes.filter(name__icontains=search_query)

    if genre_id:
        animes = animes.filter(genres__id=genre_id)

    if sort_option == 'name_asc':
        animes = animes.order_by('name')
    elif sort_option == 'name_desc':
        animes = animes.order_by('-name')
    elif sort_option == 'series_asc':
        # Считаем общее количество эпизодов через все сезоны, сортируем по убыванию
        animes = animes.annotate(
            total_episodes=db_models.Count('seasons__episodes')
        ).order_by('-total_episodes')

    genres = Genre.objects.all()

    context = {
        'anime': animes,
        'genres': genres,
        'selected_genre': genre_id,
        'search_query': search_query,
        'sort_option': sort_option,
    }
    return render(request, 'all_anime.html', context)

def films_page(request):
    return render(request, "films.html", {})

def characters_page(request):
    return render(request, "characters.html", {})

def episode_detail_page(request, episode_id):
    episode = get_object_or_404(Episode.objects.select_related('season__anime'), id=episode_id)

    context = {
        "episode": episode
    }

    return render(request, 'episode_detail.html', context)