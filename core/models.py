from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return f"{self.name}"

class Anime(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(upload_to="anime_poster")
    description = models.TextField()
    release_year = models.DateField("Дата")

    genres = models.ManyToManyField("Genre", related_name="animes")

    def save(self, *args, **kwargs):
        if not self.slug:
            allow_unicode=True 
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Anime.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        genres = ", ".join(g.name for g in self.genres.all())
        return f"Аниме: {self.name} || Жаныр: {genres} || Дата выхода: {self.release_year} || {self.slug}"

class SeasonAnime(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="seasons")
    seasons_number = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Аниме: {self.anime} || Сезон: {self.seasons_number}"

class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="anime")
    season = models.ForeignKey(SeasonAnime, on_delete=models.CASCADE, related_name="episodes")

    title = models.CharField()
    episode_number = models.PositiveIntegerField()

    video = models.FileField(upload_to="episodes/")

    def __str__(self):
        return f"Аниме: {self.anime} || Сезон: {self.season} || Называние: {self.title} || Эпизод: {self.episode_number}"

