# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.forms import UserCreationForm
from pytania.models import Pytanie, Odpowiedz, Grupa
from django.forms.models import inlineformset_factory


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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)


class GrupaForm(forms.ModelForm):
    class Meta:
        model = Grupa
        fields = ('token', )


class UserGroupForm(forms.Form):
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
            'kategoria', 'obrazek', 'typ', 'pytanie', 'tresc')
        exclude = ('autor',)
        widgets = {
            'pytanie': forms.TextInput(attrs={'size': 80}),
            'tresc': forms.Textarea(attrs={'rows': 2, 'cols': 80})}
