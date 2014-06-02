#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'tabela.views',
    url(r'^/?$', 'index', name='index'),
    url(r'^grupo/(?P<nome>\w+)/?$', 'partidas_de_grupo', name='grupo'),
    url(r'^classificacao/?$', 'classificacao', name='classificacao'),
    url(r'^classificacao/(?P<atual>\w+)/?$', 'classificacao', name='classificacao'),
    # url(r'^chaves/?$', 'chaves', name='chaves'),
    url(r'^registra_palpite/?$', 'registra_palpite', name='registra_palpite'),
    url(r'^rodada/(?P<slug>\w+)/?$', 'mostra_rodada', name='rodada'),
)
