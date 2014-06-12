from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap

admin.autodiscover()

sitemaps = {
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns(
    '',
    url(r'/?', include('tabela.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)
