# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 15:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pytania.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(help_text='Hasło dostępu do grupy testowej', max_length=128)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('grupa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='grupa', to='auth.Group')),
            ],
            options={
                'verbose_name': 'grupa',
                'verbose_name_plural': 'grupy',
            },
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'kategorie',
            },
        ),
        migrations.CreateModel(
            name='Obrazek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obrazek', models.ImageField(blank=True, null=True, upload_to=pytania.models.user_directory_path, validators=[pytania.models.validate_image], verbose_name='obrazek do pytania/odpowiedzi')),
                ('opis', models.CharField(blank=True, default='', max_length=254, verbose_name='opis obrazka')),
            ],
        ),
        migrations.CreateModel(
            name='Odpowiedz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obrazek', models.ImageField(blank=True, null=True, upload_to='odpowiedz-img', validators=[pytania.models.validate_image], verbose_name='obrazek do odpowiedzi')),
                ('tresc', models.TextField(verbose_name='treść')),
                ('czydobra', models.BooleanField(default=False, help_text='W przypadku jedno(wielo)krotnego wyboru zaznacz dobrą(e) odpowiedź(dzi)', verbose_name='dobra?')),
                ('dobraodp', models.CharField(blank=True, help_text='Dla typu pytanie – poprawna odpowiedź', max_length=254, verbose_name='Oczekiwana odpowiedź')),
            ],
            options={
                'verbose_name': 'odpowiedź',
                'verbose_name_plural': 'odpowiedzi',
            },
        ),
        migrations.CreateModel(
            name='Pytanie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[('PRO', 'Pytanie – wybór jednokrotny'), ('PCH', 'Pytanie – wybór wielokrotny'), ('PST', 'Pytanie – poprawna odpowiedź'), ('PSO', 'Pytanie – jeden wybór z listy'), ('POS', 'Pytanie – krótka odpowiedź użytkownika'), ('POL', 'Pytanie – długa odpowiedź użytkownika')], default='PRO', max_length=3)),
                ('pytanie', models.CharField(help_text='Treść pytania lub polecenie', max_length=254)),
                ('tresc', models.TextField(blank=True, help_text='Dodatkowy opis wyświetlany pod poleceniem', verbose_name='Objaśnienia')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kategoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='pytania', to='pytania.Kategoria')),
                ('obrazek', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pytania.Obrazek')),
            ],
            options={
                'verbose_name_plural': 'pytania',
                'ordering': ['kategoria'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[('T', 'Test'), ('A', 'Ankieta')], default='T', max_length=1)),
                ('nazwa', models.CharField(blank=True, default='', max_length=60)),
                ('czas', models.PositiveSmallIntegerField(default=0, verbose_name='czas rozwiązywania')),
                ('losujPyt', models.BooleanField(default=False, help_text='Losowa kolejność pytań?', verbose_name='Losuj pytania')),
                ('losujOdp', models.BooleanField(default=False, help_text='Losowa kolejność odpowiedzi?', verbose_name='Losuj odpowiedzi')),
                ('otwarty', models.BooleanField(default=False, help_text='Użytkownik może przeglądać szczegółowe wyniki?', verbose_name='Szczegółowe wyniki')),
                ('publiczny', models.BooleanField(default=False, help_text='Test dostępny dla wszystkich użytkowników?', verbose_name='Test publiczny')),
                ('ilePyt', models.BooleanField(default=False, help_text='Ilość pytań losowanych z kategorii do testu.', verbose_name='Ile wylosować pytań')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grupy', models.ManyToManyField(to='pytania.Grupa', verbose_name='Grupy przypisane do testu')),
                ('kategoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='testy', to='pytania.Kategoria')),
                ('pytania', models.ManyToManyField(to='pytania.Pytanie', verbose_name='Pytania przypisane do testu')),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'testy',
            },
        ),
        migrations.AddField(
            model_name='odpowiedz',
            name='pytanie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='odpowiedzi', to='pytania.Pytanie'),
        ),
    ]
