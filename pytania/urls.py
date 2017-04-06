# -*- coding: utf-8 -*-

from django.conf.urls import url
from pytania import views
from django.conf import settings
from django.conf.urls.static import static
# from pytania.models import Kategoria
# from django.views.generic import ListView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^konta/password/change', views.change_password, name='password-change'),
    # url(r'^register/$', views.my_register, name='register'),
    url(r'^profil/$', views.my_profil, name='profil'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^przedmioty/$', views.PrzedmiotCreate.as_view(), name='przedmioty'),
    url(r'^kategorie/$', views.KategoriaCreate.as_view(), name='kategorie'),
    url(r'^pytanie/$', views.PytanieCreate.as_view(), name='pytanie'),
    url(r'^pytania/$', views.PytaniaLista.as_view(), name='pytania-lista'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
