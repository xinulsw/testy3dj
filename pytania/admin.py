# -*- coding: utf-8 -*-

from django.contrib import admin
from pytania.models import Grupa, Kategoria
from pytania.models import Odpowiedz, Pytanie, Test
from django.forms import TextInput, Textarea
from django.db import models


@admin.register(Grupa)
class GrupaAdmin(admin.ModelAdmin):
    exclude = ('autor',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()


@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    exclude = ('autor',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()


class OdpowiedzInline(admin.TabularInline):
    model = Odpowiedz
    max_num = 6
    extra = 3
    fields = ['czydobra', 'tresc', 'dobraodp']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


class TestPytanieInline(admin.TabularInline):
    model = Test.pytania.through
    extra = 1


class TestGrupaInline(admin.TabularInline):
    model = Test.grupy.through
    extra = 1


@admin.register(Pytanie)
class PytanieAdmin(admin.ModelAdmin):
    # fields = ['przedmiot', 'kategoria', 'typ', 'polecenie']
    fieldsets = [
        (None, {'fields': [('kategoria'), 'typ', 'pytanie']}),
        ('Dodatkowe', {'fields': ['tresc'], 'classes': ['collapse']}),
    ]
    exclude = ('autor',)
    # obiekty zależne do wyświetlenia
    inlines = [OdpowiedzInline, TestPytanieInline]
    # nagłówki do wyświetlenia
    # list_display = ('question_text', 'pub_date', 'was_published_recently')
    # pole wg którego można filtrować
    list_filter = ['kategoria']
    # wyszukiwanie
    search_fields = ['pytanie']
    list_per_page = 10

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 100})},
    }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    exclude = ('autor',)
#    inlines = (TestPytanieInline, TestGrupaInline)
    list_filter = ['kategoria']
    search_fields = ['opis']
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()
