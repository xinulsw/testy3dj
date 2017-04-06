# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-22 17:02
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
                ('token', models.CharField(help_text='Has\u0142o dost\u0119pu do grupy testowej', max_length=128)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nazwa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'verbose_name': 'grupa testowa',
                'verbose_name_plural': 'grupy testowe',
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
                ('nazwa', models.CharField(max_length=50)),
                ('obrazek', models.ImageField(upload_to='obrazki')),
                ('opis', models.CharField(max_length=254, verbose_name='opis obrazka')),
            ],
        ),
        migrations.CreateModel(
            name='Odpowiedz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obrazek', models.ImageField(blank=True, null=True, upload_to='odpowiedz-img', validators=[pytania.models.validate_image], verbose_name='obrazek do odpowiedzi')),
                ('tresc', models.TextField(verbose_name='tre\u015b\u0107')),
                ('czydobra', models.BooleanField(default=False, help_text='W przypadku jedno(wielo)krotnego wyboru zaznacz dobr\u0105(e) odpowied\u017a(dzi)', verbose_name='dobra?')),
                ('dobraodp', models.CharField(blank=True, help_text='Dla typu pytanie \u2013 poprawna odpowied\u017a', max_length=254, verbose_name='Oczekiwana odpowied\u017a')),
            ],
            options={
                'verbose_name': 'odpowied\u017a',
                'verbose_name_plural': 'odpowiedzi',
            },
        ),
        migrations.CreateModel(
            name='Przedmiot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100, unique=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'przedmioty',
            },
        ),
        migrations.CreateModel(
            name='Pytanie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obrazek', models.ImageField(blank=True, null=True, upload_to='pytanie-img', validators=[pytania.models.validate_image], verbose_name='obrazek do pytania')),
                ('typ', models.CharField(choices=[('PRO', 'Pytanie \u2013 wyb\xf3r jednokrotny'), ('PCH', 'Pytanie \u2013 wyb\xf3r wielokrotny'), ('PST', 'Pytanie \u2013 poprawna odpowied\u017a'), ('PSO', 'Pytanie \u2013 jeden wyb\xf3r z listy'), ('POS', 'Pytanie \u2013 kr\xf3tka odpowied\u017a u\u017cytkownika'), ('POL', 'Pytanie \u2013 d\u0142uga odpowied\u017a u\u017cytkownika')], default='PRO', max_length=3)),
                ('polecenie', models.CharField(max_length=254, verbose_name='Polecenie')),
                ('tresc', models.TextField(blank=True, help_text='Dodatkowy opis wy\u015bwietlany pod poleceniem', verbose_name='Obja\u015bnienia')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kategoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pytania.Kategoria')),
                ('przedmiot', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pytania.Przedmiot')),
            ],
            options={
                'ordering': ['przedmiot', 'kategoria'],
                'verbose_name_plural': 'pytania',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[('T', 'Test'), ('A', 'Ankieta')], default='T', max_length=1)),
                ('opis', models.CharField(max_length=60)),
                ('czas', models.PositiveSmallIntegerField()),
                ('losujPyt', models.BooleanField(default=False, help_text='Losowa kolejno\u015b\u0107 pyta\u0144?', verbose_name='Losuj pytania')),
                ('losujOdp', models.BooleanField(default=False, help_text='Losowa kolejno\u015b\u0107 odpowiedzi?', verbose_name='Losuj odpowiedzi')),
                ('otwarty', models.BooleanField(default=False, help_text='U\u017cytkownik mo\u017ce przegl\u0105da\u0107 szczeg\xf3\u0142owe wyniki?', verbose_name='Szczeg\xf3\u0142owe wyniki')),
                ('publiczny', models.BooleanField(default=False, help_text='Test dost\u0119pny dla wszystkich u\u017cytkownik\xf3w?', verbose_name='Test publiczny')),
                ('ilePyt', models.BooleanField(default=False, help_text='Ilo\u015b\u0107 pyta\u0144 losowanych z kategorii do testu.', verbose_name='Ile losowych pyta\u0144')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grupy', models.ManyToManyField(to='pytania.Grupa', verbose_name='Grupy przypisane do test')),
                ('kategoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pytania.Kategoria')),
                ('przedmiot', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pytania.Przedmiot')),
                ('pytania', models.ManyToManyField(to='pytania.Pytanie', verbose_name='Pytania przypisane do test')),
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
        migrations.AddField(
            model_name='kategoria',
            name='przedmiot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kategorie', to='pytania.Przedmiot'),
        ),
    ]
