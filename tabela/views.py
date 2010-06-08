#!/usr/bin/env python
# encoding: utf-8

from simplejson import dumps

from django.shortcuts import *
from django.http import HttpResponseRedirect, HttpResponse, Http404

from copa_do_mundo.tabela.models import *
from copa_do_mundo import settings

def grupos(request):
    grupos = Grupo.objects.all()
    
    for grupo in grupos:
        grupo.times = Time.objects.filter(grupo__nome__exact=grupo.nome)

    return render_to_response('grupos.html', {'grupos': grupos})

def partidas(request):
    rodadas = [{'id': 'rodada_1', 'nome': '1 Rodada'}, {'id': 'rodada_2', 'nome': '2 Rodada'}, {'id': 'rodada_3', 'nome': '3 Rodada'}]
    
    for rodada in rodadas:
        rodada['partidas'] = Partida.objects.filter(rodada__exact=rodada['nome'])
    
    
    return render_to_response('partidas.html', {'rodadas': rodadas})

def registra_palpite(request):
    partida_id = request.GET['partida_id']
    try:
        palpite_time_1 = int(request.GET['palpiteTime1'])
        if palpite_time_1 < 0: palpite_time_1 = 0
    except ValueError:
        palpite_time_1 = 0
    try:
        palpite_time_2 = int(request.GET['palpiteTime2'])
        if palpite_time_2 < 0: palpite_time_2 = 0
    except ValueError:
        palpite_time_2 = 0

    partida = Partida.objects.get(id=partida_id)
    if not partida.votos:
        partida.votos = 0
        partida.palpites_time_1 = 0
        partida.palpites_time_2 = 0
    partida.votos += 1
    partida.palpites_time_1 += palpite_time_1
    partida.palpites_time_2 += palpite_time_2
    partida.save()
    return HttpResponseRedirect('/partidas.html')
