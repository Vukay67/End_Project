from django.urls import path
from .views import * 

urlpatterns = [
    path('', main_page, name="main_page"),
    path('about/', about_page, name="about_page"),
    path('contacts', contacts_page, name="contacts_page"),
    path('login/', login_page, name="login_page"),
    path('register/', register_page, name="register_page"),
    path('profil/', profil_page, name="profil_page"),
    path('anime/<str:slug>/', anime_detail_page, name="anime_detail_page"),
    path('anime/', all_anime_page, name="all_anime_page"),
    path('films/', films_page, name="films_page"),
    path('characters/', characters_page, name="characters_page"),
    path('episode/<int:episode_id>/', episode_detail_page, name='episode_detail'),
]
