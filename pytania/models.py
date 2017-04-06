# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class Grupa(models.Model):
    nazwa = models.OneToOneField(Group, unique=True)
    token = models.CharField(
        max_length=128,
        help_text="Hasło dostępu do grupy testowej")
    autor = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.nazwa
        # self.group.groupname

    class Meta:
        verbose_name = "grupa"
        verbose_name_plural = "grupy"


class Przedmiot(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    autor = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.nazwa

    class Meta:
        verbose_name_plural = "przedmioty"


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100)
    przedmiot = models.ForeignKey('Przedmiot', related_name='kategorie')
    autor = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.nazwa

    class Meta:
        verbose_name_plural = "kategorie"


class Obrazek(models.Model):
    nazwa = models.CharField(max_length=50)
    obrazek = models.ImageField(upload_to='obrazki')
    opis = models.CharField(max_length=254, verbose_name="opis obrazka")


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(
            "Maksymalny rozmiar pliku to %sMB" % str(megabyte_limit))


class Odpowiedz(models.Model):
    pytanie = models.ForeignKey('Pytanie', related_name='odpowiedzi')
    obrazek = models.ImageField(
        upload_to='odpowiedz-img',
        verbose_name="obrazek do odpowiedzi",
        null=True,
        blank=True,
        validators=[validate_image])
    tresc = models.TextField(verbose_name="treść")
    czydobra = models.BooleanField(
        default=False,
        verbose_name="dobra?",
        help_text="W przypadku jedno(wielo)krotnego wyboru zaznacz"
        " dobrą(e) odpowiedź(dzi)")
    dobraodp = models.CharField(
        max_length=254, blank=True,
        verbose_name="Oczekiwana odpowiedź",
        help_text="Dla typu pytanie – poprawna odpowiedź")

    def __unicode__(self):
        return u'%s' % "odpowiedź"

    class Meta:
        verbose_name = "odpowiedź"
        verbose_name_plural = "odpowiedzi"


class Pytanie(models.Model):
    P_SHORTTEXT = 'PST'
    P_OPENSHORT = 'POS'
    P_OPENLONG = 'POL'
    P_RADIOONE = 'PRO'
    P_CHECKBOX = 'PCH'
    P_SELECTONE = 'PSO'
    PYTANIE_TYP = (
        (P_RADIOONE, 'Pytanie – wybór jednokrotny'),
        (P_CHECKBOX, 'Pytanie – wybór wielokrotny'),
        (P_SHORTTEXT, 'Pytanie – poprawna odpowiedź'),
        (P_SELECTONE, 'Pytanie – jeden wybór z listy'),
        (P_OPENSHORT, 'Pytanie – krótka odpowiedź użytkownika'),
        (P_OPENLONG, 'Pytanie – długa odpowiedź użytkownika'),
    )
    przedmiot = models.ForeignKey(Przedmiot, default=1)
    kategoria = models.ForeignKey(Kategoria, default=1)
    obrazek = models.ImageField(
        upload_to='pytanie-img',
        verbose_name="obrazek do pytania",
        null=True,
        blank=True,
        validators=[validate_image])
    typ = models.CharField(
        max_length=3,
        choices=PYTANIE_TYP,
        default=P_RADIOONE)
    polecenie = models.CharField(max_length=254, verbose_name="Polecenie")
    tresc = models.TextField(
        blank=True,
        verbose_name="Objaśnienia",
        help_text="Dodatkowy opis wyświetlany pod poleceniem")
    autor = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.polecenie

    class Meta:
        verbose_name_plural = "pytania"
        ordering = ['przedmiot', 'kategoria']


class Test(models.Model):
    T_TEST = 'T'
    T_ANKIETA = 'A'
    TEST_TYP = (
        (T_TEST, 'Test'),
        (T_ANKIETA, 'Ankieta'),
    )
    przedmiot = models.ForeignKey(Przedmiot, default=1)
    kategoria = models.ForeignKey(Kategoria, default=1)
    typ = models.CharField(max_length=1, choices=TEST_TYP, default=T_TEST)
    opis = models.CharField(max_length=60)
    czas = models.PositiveSmallIntegerField()
    losujPyt = models.BooleanField(
        default=False,
        verbose_name="Losuj pytania",
        help_text="Losowa kolejność pytań?")
    losujOdp = models.BooleanField(
        default=False,
        verbose_name="Losuj odpowiedzi",
        help_text="Losowa kolejność odpowiedzi?")
    otwarty = models.BooleanField(
        default=False,
        verbose_name="Szczegółowe wyniki",
        help_text="Użytkownik może przeglądać szczegółowe wyniki?")
    publiczny = models.BooleanField(
        default=False,
        verbose_name="Test publiczny",
        help_text="Test dostępny dla wszystkich użytkowników?")
    ilePyt = models.BooleanField(
        default=False,
        verbose_name="Ile losowych pytań",
        help_text="Ilość pytań losowanych z kategorii do testu.")
    pytania = models.ManyToManyField(
        Pytanie,
        verbose_name="Pytania przypisane do test")
    grupy = models.ManyToManyField(
        Grupa,
        verbose_name="Grupy przypisane do test")
    autor = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.opis

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "testy"
