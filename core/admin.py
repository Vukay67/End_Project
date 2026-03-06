from django.contrib import admin
from .models import Genre, Anime, SeasonAnime, Episode

admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(SeasonAnime)
admin.site.register(Episode)