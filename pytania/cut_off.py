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