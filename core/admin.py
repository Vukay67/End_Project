from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(SeasonAnime)
admin.site.register(Episode)
admin.site.register(Film)
admin.site.register(Character)