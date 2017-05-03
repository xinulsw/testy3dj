# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Grupa(models.Model):
    grupa = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name='grupa')
    token = models.CharField(
        'Hasło',
        max_length=128,
        help_text="Hasło dostępu do grupy testowej")
    autor = models.ForeignKey(User, related_name='author')

    def __str__(self):
        return str(self.grupa)

    class Meta:
        verbose_name = "grupa"
        verbose_name_plural = "grupy"


@receiver(post_save, sender=Group)
def create_group_grupa(sender, instance, created, **kwargs):
    if created:
        Grupa.objects.create(
            grupa=instance, token=instance.token, autor=instance.autor)


@receiver(post_save, sender=Group)
def save_group_grupa(sender, instance, **kwargs):
    instance.grupa.save()


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nazwa)

    class Meta:
        verbose_name_plural = "kategorie"


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(
            "Maksymalny rozmiar pliku to %sMB" % str(megabyte_limit))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Obrazek(models.Model):
    obrazek = models.ImageField(
        upload_to=user_directory_path,
        verbose_name="obrazek do pytania/odpowiedzi",
        null=True,
        blank=True,
        validators=[validate_image])
    opis = models.CharField(
        max_length=254, verbose_name="opis obrazka", blank=True, default="")


class Odpowiedz(models.Model):
    pytanie = models.ForeignKey(
        'Pytanie', on_delete=models.CASCADE, related_name='odpowiedzi')
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

    def __str__(self):
        return "odpowiedź"

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
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.SET_DEFAULT, related_name="pytania", default=1)
    typ = models.CharField(
        max_length=3,
        choices=PYTANIE_TYP,
        default=P_RADIOONE)
    pytanie = models.CharField(
        max_length=254,
        help_text="Treść pytania lub polecenie")
    obrazek = models.ForeignKey(
        Obrazek, on_delete=models.SET_NULL, null=True)
    tresc = models.TextField(
        blank=True,
        verbose_name="Objaśnienia",
        help_text="Dodatkowy opis wyświetlany pod poleceniem")
    autor = models.ForeignKey(User)

    def __str__(self):
        return str(self.pytanie)

    class Meta:
        verbose_name_plural = "pytania"
        ordering = ['kategoria']


class Test(models.Model):
    T_TEST = 'T'
    T_ANKIETA = 'A'
    TEST_TYP = (
        (T_TEST, 'Test'),
        (T_ANKIETA, 'Ankieta'),
    )
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.SET_DEFAULT, related_name="testy", default=1)
    typ = models.CharField(max_length=1, choices=TEST_TYP, default=T_TEST)
    nazwa = models.CharField(max_length=60, blank=True, default="")
    czas = models.PositiveSmallIntegerField(
        verbose_name="czas rozwiązywania", default=0)
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
        verbose_name="Ile wylosować pytań",
        help_text="Ilość pytań losowanych z kategorii do testu.")
    pytania = models.ManyToManyField(
        Pytanie,
        verbose_name="Pytania przypisane do testu")
    grupy = models.ManyToManyField(
        Grupa,
        verbose_name="Grupy przypisane do testu")
    autor = models.ForeignKey(User)

    def __str__(self):
        return str(self.nazwa)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "testy"
