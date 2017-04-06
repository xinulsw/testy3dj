# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.forms import UserCreationForm
from pytania.models import Pytanie, Odpowiedz
from django.forms.models import inlineformset_factory


# class UserProfilForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "first_name", "last_name", "email",
# "password1", "password2")
#         help_texts = {
#             'password2': 'Podaj hasło jeszcze raz!',
#         }

#     def save(self, commit=True):
#         user = super(UserProfilForm, self).save(commit=False)
#         user.first_name = self.cleaned_data["first_name"]
#         user.last_name = self.cleaned_data["last_name"]
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user


class UserChangePassEmailForm(PasswordChangeForm):
    email = forms.EmailField(label="Email", max_length=254)


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Nazwa użytkownika", required=True)
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Imię", required=True)
    last_name = forms.CharField(label="Nazwisko", required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserGroup(forms.ModelForm):
    token = forms.CharField(label="Hasło grupy", required=True)


class ObrazekForm(forms.Form):
    imgfile = forms.FileField(label='Wybierz obrazek')


OdpowiedziFormSet = inlineformset_factory(
    Pytanie, Odpowiedz,
    fields=('obrazek', 'czydobra', 'tresc', 'dobraodp'),
    widgets={'tresc': forms.Textarea(attrs={'rows': 1, 'cols': 80})})


class PytanieForm(forms.ModelForm):
    class Meta:
        model = Pytanie
        fields = (
            'przedmiot', 'obrazek', 'kategoria', 'typ', 'polecenie', 'tresc')
        exclude = ('autor',)
        widgets = {
            'polecenie': forms.TextInput(attrs={'size': 80 }),
            'tresc': forms.Textarea(attrs={'rows': 2, 'cols': 80})}
