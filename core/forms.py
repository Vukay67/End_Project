from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class AuthenticationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Введите ваше имя пользователя"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Введите ваш пароль"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password
            )

            if not user:
                raise forms.ValidationError("Неверный логин или пароль")
            else:
                self.user = user

        return cleaned_data
    
class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "Введите ваше имя пользователя"
        })
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Введите ваше имя пользователя"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Введите ваш пароль"
        })
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Введите ваш пароль еще раз"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email):
            raise forms.ValidationError("Пользователь с таким email уже существует")
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username):
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        
        return cleaned_data