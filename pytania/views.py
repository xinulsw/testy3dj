# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import forms, authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pytania.models import Kategoria, Przedmiot, Pytanie
from pytania.forms import UserChangePassEmailForm
from django.http import HttpResponseRedirect
from pytania.forms import PytanieForm, OdpowiedziFormSet
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """Strona główna"""
    formlog = forms.AuthenticationForm()
    context = {'user': request.user, 'formlog': formlog}
    return render(request, 'pytania/index.html', context)


# def my_register(request):
#     """Rejestracja nowego użytkownika"""

#     from pytania.forms import UserProfilForm
#     form = UserProfilForm()

#     if request.method == 'POST':
#         form = UserProfilForm(request.POST)
#         if form.is_valid():
#             username = form.data['username']
#             password = form.data['password1']
#             form.save()
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, "Założono konto. Zostałeś zalogowany!")
#             return redirect(reverse('pytania:index'))

#     formlog = forms.AuthenticationForm()
#     context = {'form': form, 'formlog': formlog}
#     return render(request, 'pytania/register.html', context)

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = UserChangePassEmailForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Dane zaktualizowano!")
            return redirect('/')
        else:
            messages.error(request, 'Proszę popraw błędy!')
    else:
        form = UserChangePassEmailForm(request.user)
    return render(request, 'password_change_form.html', {
        'form': form
    })


@login_required()
def my_profil(request):
    """Edycja danych użytkownika"""

    from pytania.forms import UserUpdateForm
    data = {'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email}
    form = UserUpdateForm(initial=data)

    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane zaktualizowano!")

    formlog = forms.AuthenticationForm()
    context = {'form': form, 'formlog': formlog}
    return render(request, 'pytania/profil.html', context)


def my_login(request):
    """Logowanie użytkownika"""

    if request.method == 'POST':
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Zostałeś zalogowany!")
            return redirect(reverse('pytania:index'))

    messages.warning(request, "Proszę się zarejestrować i zalogować!")
    return redirect(reverse('pytania:index'))


def my_logout(request):
    """Wylogowywanie użytkownika z systemu"""
    logout(request)
    messages.info(request, "Zostałeś wylogowany!")
    return redirect(reverse('pytania:index'))


class PrzedmiotCreate(LoginRequiredMixin, CreateView):
    # login_url = '/pytania/login/'
    model = Przedmiot
    fields = ['nazwa']
    success_url = '/przedmioty'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Przedmiot.objects.filter(
            autor=self.request.user)
        return super(PrzedmiotCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        przedmiot = form.save(commit=False)
        przedmiot.autor = self.request.user
        przedmiot.save()
        return super(PrzedmiotCreate, self).form_valid(form)


class KategoriaCreate(LoginRequiredMixin, CreateView):
    # login_url = '/pytania/login/'
    model = Kategoria
    fields = ['nazwa', 'przedmiot']
    success_url = '/kategorie'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Kategoria.objects.filter(
            autor=self.request.user)
        return super(KategoriaCreate, self).get_context_data(**kwargs)

    def get_initial(self):
        return {
            "przedmiot": Przedmiot.objects.get(pk=1)
        }

    def form_valid(self, form):
        kategoria = form.save(commit=False)
        kategoria.autor = self.request.user
        kategoria.save()
        return super(KategoriaCreate, self).form_valid(form)


class PytanieCreate(LoginRequiredMixin, CreateView):
    login_url = '/pytania/login/'
    model = Pytanie
    form_class = PytanieForm
    success_url = '/pytanie'

    def get(self, request, *args, **kargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        odpowiedzi = OdpowiedziFormSet()
        print odpowiedzi
        return self.render_to_response(
            self.get_context_data(form=form, odpowiedzi=odpowiedzi)
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        odpowiedzi = OdpowiedziFormSet(self.request.POST)
        if form.is_valid() and odpowiedzi.is_valid():
            return self.form_valid(form, odpowiedzi)
        else:
            return self.form_invalid(form, odpowiedzi)

    def form_valid(self, form, odpowiedzi):
        pytanie = form.save(commit=False)
        pytanie.autor = self.request.user
        pytanie.save()
        self.object = pytanie
        odpowiedzi.instance = self.object
        odpowiedzi.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, odpowiedzi):
        return self.render_to_response(
            self.get_context_data(form=form, odpowiedzi=odpowiedzi)
            )


class PytaniaLista(LoginRequiredMixin, ListView):

    model = Pytanie

    def get_context_data(self, **kwargs):
        context = super(PytaniaLista, self).get_context_data(**kwargs)
        context['object_list'] = Pytanie.objects.filter(autor=self.request.user)
        return context


@login_required(login_url='/login')
def pytania(request):
    from pytania.forms import PytanieForm, OdpowiedziFormSet

    form = PytanieForm()
    odpowiedzi_formset = OdpowiedziFormSet(instance=Pytanie())

    formlog = forms.AuthenticationForm()
    context = {'form': form,
               'formlog': formlog,
               'odpowiedzi': odpowiedzi_formset}
    return render(request, 'pytania/pytania.html', context)


# from django.views.generic import ListView
# class KategoriaListView(ListView):
#    context_object_name = "kategorie"
#    queryset = Kategoria.objects.filter(autor=request.user)
#    template_name = "pytania/kategorie.html"

#    def get_queryset(self):
#        return Kategoria.objects.filter(autor=self.request.user)
