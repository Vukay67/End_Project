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
    shikimori_rating = models.PositiveIntegerField()
    our_rating = models.PositiveIntegerField()

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
    season = models.ForeignKey(SeasonAnime, on_delete=models.CASCADE, related_name="episodes")

    title = models.CharField()
    episode_number = models.PositiveIntegerField()

    video = models.FileField(upload_to="episodes/")

    def __str__(self):
        return f"Аниме: {self.season.anime} || Сезон: {self.season} || Называние: {self.title} || Эпизод: {self.episode_number}"

class Film(models.Model):
    anime = models.ForeignKey(
        Anime, 
        on_delete=models.CASCADE, 
        related_name="films",
        blank=True,          
        null=True           
    )
    title = models.CharField(max_length=200)
    release_date = models.DateField("Дата выхода", blank=True, null=True)

    def __str__(self):
        anime_name = self.anime.name if self.anime else "Без аниме"
        return f"Фильм: {self.title} || Аниме: {anime_name}"

class Character(models.Model):
    GENDER_CHOICES = [
        ['Мужской', 'Мужской'],
        ['Женский', 'Женский'],
        ['Неизвестно', 'Неизвестно']
    ]

    GG_CHOICES = [
        ['Главный герой', 'Главный герой'],
    ]

    EYE_COLOR_CHOICES = [
        ['Чёрный', 'Чёрный'],
        ['Синий', 'Синий'],
        ['Жёлтый', 'Жёлтый'],
        ['Красный', 'Красный'],
        ['Зелёный', 'Зелёный'],
        ['Фиолетывый', 'Фиолетывыё'],
    ]
    HAIR_COLOR_CHOICES = [
        ['Чёрный', 'Чёрный'],
        ['Синий', 'Синий'],
        ['Жёлтый', 'Жёлтый'],
        ['Красный', 'Красный'],
        ['Зелёный', 'Зелёный'],
        ['Фиолетывый', 'Фиолетывыё'],
    ]

    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="anime")

    eye_color = models.CharField(choices=EYE_COLOR_CHOICES)
    hair_color = models.CharField(choices=HAIR_COLOR_CHOICES)
    gender = models.CharField(choices=GENDER_CHOICES)
    species = models.CharField()
    age = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField()
    gg = models.CharField(choices=GG_CHOICES, blank=True, null=True, default="True")

    image = models.ImageField(upload_to="characters/")

    def __str__(self):
        return f"Имя: {self.name} || Пол: {self.gender} || Раса: {self.species} || Возраст: {self.age} {self.gg}"
    