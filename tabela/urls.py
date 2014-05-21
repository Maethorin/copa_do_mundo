#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'tabela.views',
    url(r'^/?$', 'index', name='index'),
    url(r'^classificacao/?$', 'grupos', name='classificacao'),
    url(r'^classificacao/atual/?$', 'grupos_atual', name='classificacao_atual'),
    url(r'^chaves/?$', 'chaves', name='chaves'),
    url(r'^partidas/?$', 'partidas', name='partidas'),
    url(r'^registra_palpite/?$', 'registra_palpite', name='registra_palpite'),
    url(r'^rodada/(?P<rodada_id>\w+)/?$', 'mostra_rodada', name='rodada'),
)
