from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AuthenticationForm, RegistrationForm
from .models import *
from django.db import models as db_models
from django.shortcuts import get_object_or_404


def main_page(request):
    anime = Anime.objects.prefetch_related('genres').all()

    context = {
        "anime": anime,
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
    character = Character.objects.filter(anime=anime).order_by('-gg')
    context = {
        "anime": anime,
        "character": character
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
    character = Character.objects.all().order_by('-gg')
    eye_colors = Character.objects.values_list('eye_color', flat=True).distinct()
    hair_colors = Character.objects.values_list('hair_color', flat=True).distinct()
    genders = Character.objects.values_list('gender', flat=True).distinct()

    search = request.GET.get('search', '')
    eye_color = request.GET.get('eye_color', '')
    hair_color = request.GET.get('hair_color', '')
    gender = request.GET.get('gender', '')

    if search:
        character = character.filter(name__icontains=search)
    if eye_color:
        character = character.filter(eye_color=eye_color)
    if hair_color:
        character = character.filter(hair_color=hair_color)
    if gender:
        character = character.filter(gender=gender)

    context = {
        "character": character,
        "eye_colors": eye_colors,
        "selected_eye": eye_color,
        "hair_colors": hair_colors,
        "selected_hair": hair_color,
        "genders": genders,
        "selected_hair": gender
    }

    return render(request, "characters.html", context)

def episode_detail_page(request, episode_id):
    episode = get_object_or_404(Episode.objects.select_related('season__anime'), id=episode_id)

    context = {
        "episode": episode
    }

    return render(request, 'episode_detail.html', context)

def all_gg_page(request):
    character = Character.objects.filter(gg="Главный герой")

    context = {
        "character": character
    }

    return render(request, "all_gg.html", context)