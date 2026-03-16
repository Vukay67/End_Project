from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(SeasonAnime)
admin.site.register(Episode)
admin.site.register(Character)
admin.site.register(Bookmark)
admin.site.register(BackgroundPicture)
admin.site.register(WatchHistory)