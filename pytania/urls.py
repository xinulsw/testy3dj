# -*- coding: utf-8 -*-

from django.conf.urls import url
from pytania import views
from django.conf import settings
from django.conf.urls.static import static
# from pytania.models import Kategoria
# from django.views.generic import ListView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^konta/password/change',
        views.change_password, name='password-change'),
    # url(r'^register/$', views.my_register, name='register'),
    url(r'^profil/$', views.my_profil, name='profil'),
    url(r'^grupy/$', views.my_grupy, name='grupy'),
    url(r'^grupa/$', views.GrupaCreate.as_view(), name='grupa'),
    url(r'^grupa/(?P<pk>\d+)/edit/$',
        views.GrupaUpdate.as_view(), name='grupa-edytuj'),
    url(r'^grupa/(?P<pk>\d+)/delete/$',
        views.GrupaDelete.as_view(), name='grupa-usun'),
    # url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^kategoria/$', views.KategoriaCreate.as_view(), name='kategoria'),
    url(r'^kategoria/(?P<pk>\d+)/edit/$',
        views.KategoriaUpdate.as_view(), name='kategoria-edytuj'),
    url(r'^kategoria/(?P<pk>\d+)/delete/$',
        views.KategoriaDelete.as_view(), name='kategoria-usun'),
    url(r'^ajax/kategoria-del/$',
        views.kategoriaDel, name='kategoria-del'),
    url(r'^pytanie/$', views.PytanieCreate.as_view(), name='pytanie'),
    url(r'^pytania/$', views.PytaniaLista.as_view(), name='pytania-lista'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
