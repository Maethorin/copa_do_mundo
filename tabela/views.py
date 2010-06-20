#!/usr/bin/env python
# encoding: utf-8
import re

from simplejson import dumps

from django.shortcuts import *
from django.http import HttpResponseRedirect, HttpResponse, Http404

from copa_do_mundo import settings

from copa_do_mundo.tabela.models import *
from copa_do_mundo.tabela import simulador

def index(request):
    return rodada(request, 'final', template='index.html')
 
def grupos(request):
    grupos = Grupo.objects.all()
    simulador.obter_dados_de_times(grupos)
    return render_to_response('grupos.html', {'grupos': grupos})

def partidas(request):
    rodadas = [
        {'id': 'rodada_1', 'nome': '1ª Rodada', 'index': 0}, 
        {'id': 'rodada_2', 'nome': '2ª Rodada', 'index': 1}, 
        {'id': 'rodada_3', 'nome': '3ª Rodada', 'index': 2},
        {'id': 'oitavas', 'nome': 'Oitavas', 'index': 3},
        {'id': 'quartas', 'nome': 'Quartas', 'index': 4},
        {'id': 'semifinais', 'nome': 'Semifinais', 'index': 5},
        {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'index': 6},
        {'id': 'final', 'nome': 'Final', 'index': 7}
    ]
    index = 0
    for rodada in rodadas:
        rodada['partidas'] = Partida.objects.filter(rodada__exact=rodada['id'])
        if not re.match('[1-3]', rodada['nome']):
            simulador.obter_times_de_partidas(rodada['partidas'])
        else:
            for partida in rodada['partidas']:
                simulador.atualiza_informacoes_de_partida_em_andamento(partida)
                partida.save()
  
    return render_to_response('partidas.html', {'rodadas': rodadas, 'index': index})

def rodada(request, rodada_id, template='partidas.html'):
    rodadas = [
        {'id': 'rodada_1', 'nome': '1ª Rodada', 'index': 0}, 
        {'id': 'rodada_2', 'nome': '2ª Rodada', 'index': 1}, 
        {'id': 'rodada_3', 'nome': '3ª Rodada', 'index': 2},
        {'id': 'oitavas', 'nome': 'Oitavas', 'index': 3},
        {'id': 'quartas', 'nome': 'Quartas', 'index': 4},
        {'id': 'semifinais', 'nome': 'Semifinais', 'index': 5},
        {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'index': 6},
        {'id': 'final', 'nome': 'Final', 'index': 7}
    ]
    index = 0
    for rodada in rodadas:
        if rodada['id'] == rodada_id:
            rodada['partidas'] = Partida.objects.filter(rodada__exact=rodada['id'])
            index = rodada['index']
            if not re.match('[1-3]', rodada['nome']):
                simulador.obter_times_de_partidas(rodada['partidas'])
            else:
                for partida in rodada['partidas']:
                    simulador.atualiza_informacoes_de_partida_em_andamento(partida)
                    partida.save()

    return render_to_response(template, {'rodadas': rodadas, 'rodada_id': rodada_id, 'index': index})
    
def registra_palpite(request):
    json = request.GET.get('json', '') == 'json'
    partida_id = request.GET['partida_id']
    rodada_id = request.GET['rodada_id']
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
    if partida.em_andamento():
        return HttpResponseRedirect('/rodada/%s' % rodada_id)

    if not partida.votos:
        partida.votos = 0
        partida.palpites_time_1 = 0
        partida.palpites_time_2 = 0
    partida.votos += 1
    partida.palpites_time_1 += palpite_time_1
    partida.palpites_time_2 += palpite_time_2
    partida.save()
    if json:
        return HttpResponse('{"partida_id": "partida_%s", "gols_time_1": %s, "gols_time_2": %s, "votos": %s}' % (partida.id, partida.media_palpites_time_1(), partida.media_palpites_time_2(), partida.votos), mimetype="text/json")

    return HttpResponseRedirect('/rodada/%s' % rodada_id)
