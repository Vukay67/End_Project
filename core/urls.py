from django.urls import path
from .views import main_page, about_page, contacts_page, login_page, register_page

urlpatterns = [
    path('', main_page, name="main_page"),
    path('about/', about_page, name="about_page"),
    path('contacts', contacts_page, name="contacts_page"),
    path('login/', login_page, name="login_page"),
    path('register/', register_page, name="register_page")
]
