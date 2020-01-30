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
    some_field = forms.CharField(max_length=254, help_text='Кастомное поле-полюшко')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == 'a@a.aa':
            raise forms.ValidationError('Эта почта запрещена частным законом')
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        some_field = cleaned_data.get("some_field")
        email = cleaned_data.get("email")

        if email == 'a@a.aa':
            raise forms.ValidationError('Эта почта запрещена общим законом')

        if some_field and int(some_field) < 100:
            raise forms.ValidationError(
                "Some field is smaller than 100"
            )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        labels = { 'username': 'Ваш логин', }
        help_texts = { 'username': 'Ваш неповторимый логин' }
