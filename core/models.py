from django.db import models

class Anime(models.Model):
    name = models.CharField()
    image = models.ImageField(upload_to="anime_poster")
    description = models.TextField()

class SesonAnime(models.Model):
    pass

