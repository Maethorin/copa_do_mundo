from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^favicon\.ico$', 'django.shortcuts.redirect', {'url': '/static/images/favicon.ico'}),
    url(r'/?', include('tabela.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
