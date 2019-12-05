from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(max_length=254, help_text='Обязательное поле')
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=254,
        help_text="Ваш пароль"
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=254, help_text='Обязательное поле')
    email = forms.EmailField(max_length=254, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
