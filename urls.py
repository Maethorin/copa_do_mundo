#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls.defaults import *
from copa_do_mundo import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
     (r'^', include('copa_do_mundo.tabela.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)', 'copa_do_mundo.static_serve.serve_media',
                                name='serve_media_file'),
    )