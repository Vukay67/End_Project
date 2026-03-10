from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AuthenticationForm, RegistrationForm
from .models import *
from django.db import models as db_models
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery
from random import choices


def main_page(request):
    user = request.user
    anime = Anime.objects.prefetch_related('genres').all()
    top_ani = Anime.objects.filter(our_rating__gte=4.5)

    planned_anime = None

    if request.user.is_authenticated:
        planned_anime_qs = Anime.objects.filter(
            bookmark__user=request.user,
            bookmark__status='planned'
        )

        if planned_anime_qs.exists():
            planned_anime = choices(planned_anime_qs)

    ran_ani = choices(top_ani) if top_ani else None
    ran_ani1 = choices(top_ani) if top_ani else None
    ran_ani2 = choices(top_ani) if top_ani else None

    context = {
        "anime": anime,
        "ran_ani": ran_ani,
        "ran_ani1": ran_ani1,
        "ran_ani2": ran_ani2,
        "nex_ani": planned_anime
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

def anime_detail_page(request, slug):
    anime = get_object_or_404(
        Anime.objects.prefetch_related('genres', 'seasons__episodes'),
        slug=slug
    )
    current_bookmark = None
    current_reating = None

    if request.user.is_authenticated:
        bookmark = Bookmark.objects.filter(user=request.user, anime=anime).first()
        if bookmark:
            current_bookmark = bookmark.status

    if request.user.is_authenticated:
        point = Reating.objects.filter(user=request.user, anime=anime).first()
        if point:
            current_reating = point.point

    character = Character.objects.filter(anime=anime).order_by('-gg')
    context = {
        "anime": anime,
        "character": character,
        'current_bookmark': current_bookmark,
        "current_reating": current_reating
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

def characters_page(request):
    search_query = request.GET.get('search', '')
    selected_eye = request.GET.get('eye_color', '')
    selected_hair = request.GET.get('hair_color', '')
    selected_gender = request.GET.get('gender', '')
    selected_specie = request.GET.get('specie', '')

    characters = Character.objects.select_related('anime').all()

    if search_query:
        characters = characters.filter(name__icontains=search_query)
    if selected_eye:
        characters = characters.filter(eye_color=selected_eye)
    if selected_hair:
        characters = characters.filter(hair_color=selected_hair)
    if selected_gender:
        characters = characters.filter(gender=selected_gender)
    if selected_specie:
        characters = characters.filter(species=selected_specie)

    context = {
        'character': characters,
        'eye_colors':  Character.EYE_COLOR_CHOICES,
        'hair_colors': Character.HAIR_COLOR_CHOICES,
        'genders':     Character.GENDER_CHOICES,
        'species':     Character.SPECIES_CHOICES,
        'search_query':    search_query,
        'selected_eye':    selected_eye,
        'selected_hair':   selected_hair,
        'selected_genders': selected_gender,
        'selected_specie': selected_specie,
    }
    return render(request, 'characters.html', context)

def episode_detail_page(request, episode_id):
    episode = get_object_or_404(Episode.objects.select_related('season__anime'), id=episode_id)
    characters = Character.objects.filter(anime=episode.season.anime, gg="Главный герой")

    prev_episode = Episode.objects.filter(
        season=episode.season,
        episode_number=episode.episode_number - 1
    ).first()

    next_episode = Episode.objects.filter(
        season=episode.season,
        episode_number=episode.episode_number + 1
    ).first()

    context = {
        "characters": characters,
        "episode": episode,
        "prev_episode": prev_episode,
        "next_episode": next_episode,
    }
    return render(request, 'episode_detail.html', context)

def all_gg_page(request):
    character = Character.objects.filter(gg="Главный герой")
    search_query = request.GET.get('search', '')
    selected_eye = request.GET.get('eye_color', '')
    selected_hair = request.GET.get('hair_color', '')
    selected_gender = request.GET.get('gender', '')
    selected_specie = request.GET.get('specie', '')

    if search_query:
        character = character.filter(name__icontains=search_query)
    if selected_eye:
        character = character.filter(eye_color=selected_eye)
    if selected_hair:
        character = character.filter(hair_color=selected_hair)
    if selected_gender:
        character = character.filter(gender=selected_gender)
    if selected_specie:
        character = character.filter(species=selected_specie)

    context = {
        "character": character,
        'eye_colors':  Character.EYE_COLOR_CHOICES,
        'hair_colors': Character.HAIR_COLOR_CHOICES,
        'genders':     Character.GENDER_CHOICES,
        'species':     Character.SPECIES_CHOICES,
        'search_query':    search_query,
        'selected_eye':    selected_eye,
        'selected_hair':   selected_hair,
        'selected_genders': selected_gender,
        'selected_specie': selected_specie,
    }
    return render(request, "all_gg.html", context)

@login_required
def add_bookmark(request, slug, status):
    anime = get_object_or_404(Anime, slug=slug)
    if status == 'delete':
        Bookmark.objects.filter(user=request.user, anime=anime).delete()
    else:
        Bookmark.objects.update_or_create(
            user=request.user,
            anime=anime,
            defaults={"status": status}
        )
    return redirect("anime_detail_page", slug=slug)

@login_required
def add_reating(request, slug, point):
    anime = get_object_or_404(Anime, slug=slug)
    if point == 'delete':
        Reating.objects.filter(user=request.user, anime=anime).delete()
    else:
        Reating.objects.update_or_create(
            user=request.user,
            anime=anime,
            defaults={"point": point}
        )
    return redirect("anime_detail_page", slug=slug)

def redact_page(request):
    return render(request, "redact.html", {})

@login_required
def profil_page(request):
    user = request.user

    rating_sub = Reating.objects.filter(
        user=user, anime=OuterRef('anime')
    ).values('point')[:1]

    watched = user.bookmark_set.filter(status='watched').annotate(
        user_rating=Subquery(rating_sub)
    )
    planned = user.bookmark_set.filter(status='planned')

    context = {
        'watched': watched,
        'planned': planned,
    }
    return render(request, "profil.html", context)
