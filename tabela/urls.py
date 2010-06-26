#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls.defaults import *
from copa_do_mundo.tabela import views

urlpatterns = patterns('',
    url(r'^$', 'copa_do_mundo.tabela.views.index', name='index'),
    url(r'^index.html', 'copa_do_mundo.tabela.views.index', name='index'),
    url(r'^classificacao.html', 'copa_do_mundo.tabela.views.grupos', name='grupos'),
    url(r'^classificacao_atual.html', 'copa_do_mundo.tabela.views.grupos_atual', name='grupos_atual'),
    url(r'^chaves.html', 'copa_do_mundo.tabela.views.chaves', name='chaves'),
    url(r'^partidas.html', 'copa_do_mundo.tabela.views.partidas', name='partidas'),
    url(r'^registra_palpite', 'copa_do_mundo.tabela.views.registra_palpite', name='registra_palpite'),
    url(r'^rodada/(\w.+)/$', 'copa_do_mundo.tabela.views.rodada', name='rodada'),
)
