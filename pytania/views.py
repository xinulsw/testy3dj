# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import forms, logout  # authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pytania.models import Grupa, Kategoria, Obrazek, Pytanie
from django.contrib.auth.models import Group
from pytania.forms import UserChangePassEmailForm
from pytania.forms import GroupForm, GrupaForm
from django.http import HttpResponseRedirect
from pytania.forms import PytanieForm, OdpowiedziFormSet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    """Strona główna"""
    formlog = forms.AuthenticationForm()
    context = {'user': request.user, 'formlog': formlog}
    return render(request, 'pytania/index.html', context)


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
    from pytania.forms import UserGroupForm
    user_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        if user_form.has_changed() and user_form.is_valid():
            user_form.save()
            messages.success(request, "Dane zaktualizowano!")
        else:
            messages.info(request, "Dane są aktualne.")

    # formlog = forms.AuthenticationForm()
    grupa_form = UserGroupForm()
    grupy = request.user.groups.all()
    context = {
        'user_form': user_form,
        'grupa_form': grupa_form,
        'grupy': grupy
    }
    return render(request, 'pytania/profil.html', context)


def my_logout(request):
    """Wylogowywanie użytkownika z systemu"""
    logout(request)
    messages.info(request, "Zostałeś wylogowany!")
    return redirect(reverse('pytania:index'))


@login_required()
def my_grupy(request):
    """Dodawanie do grupy / lista grup / usuwanie z grupy użytkownika"""

    from pytania.forms import UserUpdateForm
    from pytania.forms import UserGroupForm

    if request.method == 'POST':
        grupa_form = UserGroupForm(data=request.POST)
        if grupa_form.is_valid():
            try:
                grupa = Grupa.objects.get(
                    token=grupa_form.cleaned_data.get('token'))
                if request.user.groups.filter(pk=grupa.grupa.id).count():
                    messages.warning(
                        request, 'Jesteś już w grupie %s!' % grupa.grupa)
                else:
                    grupa.grupa.user_set.add(request.user)
                    messages.success(
                        request, "Dodano Cię do grupy %s!" % grupa.grupa)
            except Grupa.DoesNotExist:
                messages.error(request, 'Błędne hasło!')

        # usnięcie użytkownika z grup
        if request.POST.get('grupydel'):
            for g_id in request.POST.get('grupydel'):
                grupa = Grupa.objects.get(grupa=g_id)
                grupa.grupa.user_set.remove(request.user)
                messages.success(
                    request, "Usunięto Cię z grupy %s!" % grupa.grupa)

    user_form = UserUpdateForm(instance=request.user)
    grupa_form = UserGroupForm()
    grupy = request.user.groups.all()
    context = {
        'user_form': user_form,
        'grupa_form': grupa_form,
        'grupy': grupy
    }
    return render(request, 'pytania/profil.html', context)


# def test_func(user):
#     """Czy użytkowni jest w grupie Autorzy?"""
#     return user.groups.filter(name='Autorzy').exists()


@login_required
# @user_passes_test(test_func)
# @transaction.atomic
def update_grupa(request, group_id=None):

    if not request.user.groups.filter(name='Autorzy').exists():
        messages.warning(
            request,
            "Aby dodawać grupy, musisz należeć do grupy Autorzy")
        return redirect('/grupy/')

    object_list = Grupa.objects.filter(autor=request.user)

    if (group_id):
        group = Group.objects.select_related('grupa').get(pk=group_id)
    else:
        group = Group()
        group.grupa = Grupa()

    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        grupa_form = GrupaForm(request.POST, instance=group.grupa)
        grupa_form.instance.autor = request.user
        if group_form.is_valid() and grupa_form.is_valid():
            group_form.instance.autor = request.user
            group_form.instance.token = grupa_form.instance.token
            group_form.save()
            # grupa_form.instance.grupa = obj
            # grupa_form.save()
            messages.success(request, ('Dodano grupę'))
            return redirect('pytania:grupa')
        else:
            messages.error(request, ('Popraw poniższe błędy.'))
    else:
        group_form = GroupForm(instance=group)
        grupa_form = GrupaForm(instance=group.grupa)

    return render(request, 'pytania/grupa_form.html', {
        'object_list': object_list,
        'group_form': group_form,
        'grupa_form': grupa_form
    })


class GrupaDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    template_name_suffix = '_delete'
    success_url = '/grupa'

    def test_func(self):
        """Nadpisanie funkcji testującej uprawnienia użytkownika"""
        return self.request.user.groups.filter(name='Autorzy').exists()

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(GrupaDelete, self).get_login_url()
        else:
            self.redirect_field_name = None
            messages.warning(
                self.request,
                "Aby usuwać grupy, musisz należeć do grupy Autorzy")
            return '/grupy/'


class KategoriaCreate(LoginRequiredMixin, CreateView):
    # login_url = '/pytania/login/'
    model = Kategoria
    fields = ['nazwa']
    success_url = '/kategoria'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Kategoria.objects.filter(
            autor=self.request.user)
        return super(KategoriaCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        kategoria = form.save(commit=False)
        kategoria.autor = self.request.user
        kategoria.save()
        return super(KategoriaCreate, self).form_valid(form)


class KategoriaUpdate(LoginRequiredMixin, UpdateView):
    # login_url = '/pytania/login/'
    model = Kategoria
    fields = ['nazwa']
    success_url = '/kategoria'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Kategoria.objects.filter(
            autor=self.request.user)
        return super(KategoriaUpdate, self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     kategoria = form.save(commit=False)
    #     kategoria.autor = self.request.user
    #     kategoria.save()
    #     return super(KategoriaUpdate, self).form_valid(form)


class KategoriaDelete(LoginRequiredMixin, DeleteView):
    model = Kategoria
    template_name_suffix = '_delete'
    success_url = '/kategoria'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(KategoriaDelete, self).form_valid(form)


def kategoriaDel(request):
    from django.http import JsonResponse
    data = {}
    if request.method == 'POST':
        kategoria_id = request.POST.get('kategoria-id')
        if kategoria_id:
            data['success'] = 'Kategorię usunięto!'
    else:
        data['error'] = 'To nie powinno się zdarzyć!'

    return JsonResponse(data)


class ObrazekCreate(LoginRequiredMixin, CreateView):
    model = Obrazek
    fields = ['obrazek', 'opis', 'kategoria']
    success_url = '/obrazek'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Obrazek.objects.filter(
            autor=self.request.user)
        return super(ObrazekCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.autor = self.request.user
        obj.save()
        return super(ObrazekCreate, self).form_valid(form)


class ObrazekUpdate(LoginRequiredMixin, UpdateView):
    model = Obrazek
    fields = ['obrazek', 'opis', 'kategoria']
    success_url = '/obrazki'


class ObrazekDelete(LoginRequiredMixin, DeleteView):
    model = Obrazek
    fields = ['obrazek', 'opis', 'kategoria']
    success_url = '/obrazki'


class PytanieCreate(LoginRequiredMixin, CreateView):
    # login_url = '/pytania/login/'
    model = Pytanie
    form_class = PytanieForm
    success_url = '/pytanie'

    def get(self, request, *args, **kargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        odpowiedzi = OdpowiedziFormSet()
        print(odpowiedzi)
        return self.render_to_response(
            self.get_context_data(form=form, odpowiedzi=odpowiedzi))

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
        context['object_list'] = Pytanie.objects.filter(
            autor=self.request.user)
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
