from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.functions import Cast
from django.db.models import FloatField, Avg

# ================== Genre ==================
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ================== Anime ==================
class Anime(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="anime_poster")
    description = models.TextField()
    release_year = models.DateField("Дата")
    shikimori_rating = models.DecimalField(max_digits=3, decimal_places=1)
    our_rating = models.FloatField(default=0)  # Автоматически обновляемое поле

    genres = models.ManyToManyField("Genre", related_name="animes")

    def save(self, *args, **kwargs):
        if not self.slug:
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
        return f"Аниме: {self.name} || Жанр: {genres} || Дата выхода: {self.release_year} || {self.slug}"

# ================== Bookmark ==================
class Bookmark(models.Model):
    STATUS_CHOICES = [
        ['planned', 'Буду смотреть'],
        ['watched', 'Просмотрено'],
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("user", "anime")

    def __str__(self):
        return f"{self.user} - {self.anime} ({self.status})"
    
# ================== Reating ==================
class Reating(models.Model):
    REATING_CHOICES = [
        ['1', '⭐1'],
        ['2', '⭐2'],
        ['3', '⭐3'],
        ['4', '⭐4'],
        ['5', '⭐5'],
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    point = models.CharField(max_length=5, choices=REATING_CHOICES)

    class Meta:
        unique_together = ("user", "anime")

    def __str__(self):
        return f"{self.user} - {self.anime} ({self.point})"

# ================== SeasonAnime ==================
class SeasonAnime(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="seasons")
    seasons_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Аниме: {self.anime} || Сезон: {self.seasons_number}"

# ================== Episode ==================
class Episode(models.Model):
    season = models.ForeignKey(SeasonAnime, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=200)
    episode_number = models.PositiveIntegerField()
    video = models.FileField(upload_to="episodes/")

    def __str__(self):
        return f"Аниме: {self.season.anime} || Сезон: {self.season.seasons_number} || Название: {self.title} || Эпизод: {self.episode_number}"

# ================== Film ==================
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

# ================== Character ==================
class Character(models.Model):
    GENDER_CHOICES = [
        ['Мужской',    '♂️ Мужской'],
        ['Женский',    '♀️ Женский'],
        ['Неизвестно', '❓ Неизвестно'],
    ]

    GG_CHOICES = [
        ['Главный герой', '⭐ Главный герой'],
    ]

    EYE_COLOR_CHOICES = [
        ['Красный', '🔴 Красный'],
        ['Оранжевый', '🟠 Оранжевый'],
        ['Жёлтый', '🟡 Жёлтый'],
        ['Зелёный', '🟢 Зелёный'],
        ['Синий', '🔵 Синий'],
        ['Фиолетовый', '🟣 Фиолетовый'],
        ['Коричневый', '🟤 Коричневый'],
        ['Чёрный', '⚫️ Чёрный'],
        ['Белый', '⚪️ Белый'],
    ]

    HAIR_COLOR_CHOICES = EYE_COLOR_CHOICES.copy()

    SPECIES_CHOICES = [
        ['Человек', 'Человек'],
        ['Демон',   'Демон'],
        ['Ангел',   'Ангел'],
        ['Гном',    'Гном'],
        ['Эльф',    'Эльф'],
    ]

    anime      = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="characters")
    eye_color  = models.CharField(max_length=20, choices=EYE_COLOR_CHOICES)
    hair_color = models.CharField(max_length=20, choices=HAIR_COLOR_CHOICES)
    gender     = models.CharField(max_length=20, choices=GENDER_CHOICES)
    species    = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    age        = models.PositiveIntegerField(blank=True, null=True)
    name       = models.CharField(max_length=100)
    gg         = models.CharField(max_length=20, choices=GG_CHOICES, blank=True, null=True, default=None)
    image      = models.ImageField(upload_to="characters/")

    def __str__(self):
        return f"Имя: {self.name} || Пол: {self.gender} || Раса: {self.species} || Возраст: {self.age} || {self.gg}"
    
@receiver(post_save, sender=Reating)
@receiver(post_delete, sender=Reating)
def update_anime_rating(sender, instance, **kwargs):
    anime = instance.anime
    avg = Reating.objects.filter(anime=anime).aggregate(
        avg=Avg(Cast('point', FloatField()))
    )['avg'] or 0
    Anime.objects.filter(pk=anime.pk).update(our_rating=round(avg, 1))

class BackgroundPicture(models.Model):
    image = models.ImageField(upload_to="background/")