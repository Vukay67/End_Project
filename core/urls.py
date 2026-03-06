from django.urls import path
from .views import main_page, about_page, contacts_page, login_page, register_page, profil_page, anime_detail_page, all_anime_page

urlpatterns = [
    path('', main_page, name="main_page"),
    path('about/', about_page, name="about_page"),
    path('contacts', contacts_page, name="contacts_page"),
    path('login/', login_page, name="login_page"),
    path('register/', register_page, name="register_page"),
    path('profil/', profil_page, name="profil_page"),
    path('anime/<str:slug>/', anime_detail_page, name="anime_detail_page"),
    path('anime/', all_anime_page, name="all_anime_page")
]
