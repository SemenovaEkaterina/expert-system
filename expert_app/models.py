from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import models
from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'me', }
        ),
        max_length=30,
        label=u'Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '*******', }
        ),
        label=u'Пароль'
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''),
                            password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(u'Данный пользователь не активен')
        else:
            raise forms.ValidationError(u'Указан неверный логин или пароль')


class SignupForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'me', }),
        max_length=30, label=u'Логин'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': u'Александр', }),
        max_length=30, label=u'Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': u'Иванник', }),
        max_length=30, label=u'Фамилия'
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'me@gmail.com', }),
        required=False, max_length=254, label=u'E-mail'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '*****'}),
        min_length=6, label=u'Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '*****'}),
        min_length=6, label=u'Повторите пароль'
    )

    def clean_login(self):
        login = self.cleaned_data.get('login', '')

        try:
            u = User.objects.get(username=login)
            raise forms.ValidationError(u'Такой пользователь уже существует')
        except User.DoesNotExist:
            return login

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('login')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        return authenticate(username=u.username, password=password)
