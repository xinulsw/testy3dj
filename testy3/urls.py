from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'testy3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('pytania.urls', namespace='pytania')),
    url(r'^pytania/', include('pytania.urls', namespace='pytania')),
    url(r'^konta/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
