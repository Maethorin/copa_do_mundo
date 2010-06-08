#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^grupos.html', 'tabela.views.grupos', name='grupos'),
    url(r'^partidas.html', 'tabela.views.partidas', name='partidas'),
    url(r'^registra_palpite', 'tabela.views.registra_palpite', name='registra_palpite'),
)