#!/usr/bin/env python
# encoding: utf-8
import re

from django.shortcuts import *

from copa_do_mundo import settings

from copa_do_mundo.tabela.models import *
from copa_do_mundo.tabela import simulador


def index(request):
    return rodada(request, 'final', template='index.html', inclui_partida_em_andamento=True)


def grupos(request):
    grupos = Grupo.objects.all()
    simulador.obter_dados_de_times(grupos)
    return render_to_response('grupos.html', {'grupos': grupos, 'atual': False})


def grupos_atual(request):
    grupos = Grupo.objects.all()
    simulador.obter_dados_de_times(grupos, atual=True)
    return render_to_response('grupos.html', {'grupos': grupos, 'atual': True})


def chaves(request):
    rodadas = _obter_rodadas(mata_mata=True)
    return partidas(request, rodadas, template='chaves.html', eh_chaves=True)


def partidas(request, rodadas=None, template='partidas.html', eh_chaves=False):
    if not rodadas:
        rodadas = _obter_rodadas()
    index = 0
    for rodada in rodadas:
        rodada['partidas'] = Partida.objects.filter(rodada__exact=rodada['id'])
        if not re.match('[1-3]', rodada['nome']):
            simulador.obter_times_de_partidas(rodada['partidas'])
        else:
            for partida in rodada['partidas']:
                simulador.atualiza_informacoes_de_partida_em_andamento(partida)
                partida.save()
        if eh_chaves:
            simulador.reordena_partidas_para_chave(rodada)
    return render_to_response(template, {'rodadas': rodadas, 'index': index, 'chaves': eh_chaves})


def rodada(request, rodada_id, template='partidas.html', inclui_partida_em_andamento=False):
    rodadas = _obter_rodadas()
    index = 0
    rodadas[0]['partidas'] = simulador.obter_partidas_em_andamento()
    for partida in rodadas[0]['partidas']:
        simulador.atualiza_informacoes_de_partida_em_andamento(partida)
        partida.save()

    for rodada in rodadas:
        if rodada['id'] == rodada_id and rodada_id != 'em_andamento':
            rodada['partidas'] = Partida.objects.filter(rodada__exact=rodada['id'])
            index = rodada['index']
            if not re.match('[1-3]', rodada['nome']):
                simulador.obter_times_de_partidas(rodada['partidas'])

    return render_to_response(template, {'rodadas': rodadas, 'rodada_id': rodada_id, 'index': index})


def registra_palpite(request):
    json = request.GET.get('json', '') == 'json'
    chaves = request.GET.get('chaves', '') == 'chaves'
    partida_id = request.GET['partida_id']
    rodada_id = request.GET['rodada_id']
    palpite_time_1 = 0
    palpite_time_2 = 0

    palpite_time_1, palpite_time_2 = _obtem_palpites(request)

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
    
    if chaves:
        return HttpResponseRedirect('/chaves.html')

    return HttpResponseRedirect('/rodada/%s' % rodada_id)


def _obtem_palpites(request):
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

    if palpite_time_1 > 7:
        palpite_time_1 = 0

    if palpite_time_2 > 7:
        palpite_time_2 = 0
        
    return palpite_time_1, palpite_time_2


def _obter_rodadas(mata_mata=False):
    rodadas = []
    if not mata_mata:
        rodadas.extend([
            {'id': 'em_andamento', 'nome': 'Em Andamento', 'index': 0},
            {'id': 'rodada_1', 'nome': '1ª Rodada', 'index': 1}, 
            {'id': 'rodada_2', 'nome': '2ª Rodada', 'index': 2}, 
            {'id': 'rodada_3', 'nome': '3ª Rodada', 'index': 3}
        ])

    rodadas.extend([
        {'id': 'oitavas', 'nome': 'Oitavas', 'index': 4},
        {'id': 'quartas', 'nome': 'Quartas', 'index': 5},
        {'id': 'semifinais', 'nome': 'Semifinais', 'index': 6}
        
    ])
    
    if mata_mata:
        rodadas.extend([
            {'id': 'final', 'nome': 'Final', 'index': 8},
            {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'index': 7}
        ])
    else:
        rodadas.extend([
            {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'index': 7},
            {'id': 'final', 'nome': 'Final', 'index': 8}
        ])
    
    return rodadas