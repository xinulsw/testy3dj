# -*- coding: utf-8 -*-

# models.py
# from __future__ import unicode_literals

# class Przedmiot(models.Model):
#     nazwa = models.CharField(max_length=100, unique=True)
#     autor = models.ForeignKey(User)

#     def str(self):
#         return self.nazwa

#     class Meta:
#         verbose_name_plural = "przedmioty"

# przedmiot = models.ForeignKey('Przedmiot', related_name='kategorie')
# przedmiot = models.ForeignKey(Przedmiot, default=1)
# przedmiot = models.ForeignKey(Przedmiot, default=1)

# views.py

class GrupaCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Group
    # fields = ['name', 'token']
    form_class = NewGroupForm
    template_name = 'pytania/grupa_form.html'
    success_url = "/grupa"

    def test_func(self):
        """Nadpisanie funkcji testującej uprawnienia użytkownika"""
        return self.request.user.groups.filter(name='Autorzy').exists()

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(GrupaCreate, self).get_login_url()
        else:
            self.redirect_field_name = None
            messages.warning(
                self.request,
                "Aby dodawać grupy, musisz należeć do grupy Autorzy")
            return '/grupy/'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Grupa.objects.filter(
            autor=self.request.user)
        return super(GrupaCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        print(self.object)
        grupa = Grupa(
            grupa=self.object,
            token=form.cleaned_data['token'],
            autor=self.request.user)
        grupa.save()
        return super(GrupaCreate, self).form_valid(form)

    # def save(self, *args, **kwargs):
    #         self.full_clean()
    #         super(Room, self).save(*args, **kwargs)


class GrupaUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    form_class = NewGroupForm
    template_name = 'pytania/grupa_form.html'
    success_url = "/grupa"

    def test_func(self):
        """Nadpisanie funkcji testującej uprawnienia użytkownika"""
        return self.request.user.groups.filter(name='Autorzy').exists()

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(GrupaUpdate, self).get_login_url()
        else:
            self.redirect_field_name = None
            messages.warning(
                self.request,
                "Aby edytować grupy, musisz należeć do grupy Autorzy")
            return '/grupy/'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Grupa.objects.filter(
            autor=self.request.user)
        return super(GrupaUpdate, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.initial = {'token': self.object.grupa.token}
            print(self.object.grupa.token)
        except Grupa.DoesNotExist:
            pass
        return super(GrupaUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NewGroupForm(self.request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        # self.object.save()
        grupa = Grupa.objects.get(grupa=self.object)
        if grupa.token != form.cleaned_data['token']:
            grupa.token = form.cleaned_data['token']
            grupa.save()
        return super(GrupaUpdate, self).form_valid(form)


class GrupaDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grupa
    template_name_suffix = '_delete'
    success_url = '/grupa'

    def test_func(self):
        """Nadpisanie funkcji testującej uprawnienia użytkownika"""
        return self.request.user.groups.filter(name='Autorzy').exists()

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(GrupaCreate, self).get_login_url()
        else:
            self.redirect_field_name = None
            messages.warning(
                self.request,
                "Aby usuwać grupy, musisz należeć do grupy Autorzy")
            return '/grupy/'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(GrupaDelete, self).form_valid(form)

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

# def my_login(request):
#     """Logowanie użytkownika"""

#     if request.method == 'POST':
#         form = forms.AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, "Zostałeś zalogowany!")
#             return redirect(reverse('pytania:index'))

#     messages.warning(request, "Proszę się zarejestrować i zalogować!")
#     return redirect(reverse('pytania:index'))


# class PrzedmiotCreate(LoginRequiredMixin, CreateView):
#     # login_url = '/pytania/login/'
#     model = Przedmiot
#     fields = ['nazwa']
#     success_url = '/przedmioty'

#     def get_context_data(self, **kwargs):
#         kwargs['object_list'] = Przedmiot.objects.filter(
#             autor=self.request.user)
#         return super(PrzedmiotCreate, self).get_context_data(**kwargs)

#     def form_valid(self, form):
#         przedmiot = form.save(commit=False)
#         przedmiot.autor = self.request.user
#         przedmiot.save()
#         return super(PrzedmiotCreate, self).form_valid(form)

# def get_initial(self):
#     return {
#         "przedmiot": Przedmiot.objects.get(pk=1)
#     }


# admin.py
# admin.site.register(Grupa, GrupaAdmin)

# @admin.register(Przedmiot)
# class PrzedmiotAdmin(admin.ModelAdmin):
#     exclude = ('autor',)

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.autor = request.user
#         obj.save()


# admin.site.register(Przedmiot, PrzedmiotAdmin)
# admin.site.register(Kategoria, KategoriaAdmin)
# admin.site.register(Test, TestAdmin)
# admin.site.register(Pytanie, PytanieAdmin)

# forms.py
# class UserProfilForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "first_name", "last_name", "email",
# "password1", "password2")
#         help_texts = {
#             'password2': 'Podaj hasło jeszcze raz!',
#         }

#     def save(self, commit=True):
#         user = super(UserProfilForm, self).save(commit=False)
#         user.first_name = self.cleaned_data["first_name"]
#         user.last_name = self.cleaned_data["last_name"]
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user

# urls.py
# url(r'^przedmioty/$', views.PrzedmiotCreate.as_view(), name='przedmioty'),
