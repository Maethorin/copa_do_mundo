#!/usr/bin/env python
# encoding: utf-8
import re
from django.core.context_processors import csrf

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from tabela.models import Grupo, Partida, Fase
from tabela import simulador


def index(request):
    return render_to_response(
        'index.html',
        {
            'grupos': Grupo.objects.all(),
            'titulo_da_pagina': 'Inicial',
            'css_fundo': 'inicial'
        }
    )


@csrf_protect
def grupo(request, nome):
    grupos = Grupo.objects.all()
    grupo = Grupo.objects.get(nome=nome)
    partidas_do_grupo = simulador.obtem_partidas_de_grupo(grupo)
    contexto =         {
            'grupos': grupos, 'grupo': grupo, 'pagina_atual': grupo.nome, 'em_grupos': True, 'ja_votou': True,
            'partidas': partidas_do_grupo, 'css_fundo': 'grupos', 'titulo_da_pagina': "Grupo {}".format(grupo.nome)
        }

    contexto.update(csrf(request))
    return render_to_response(
        'grupo.html',
        contexto
    )


def classificacao(request, atual=None):
    atual = atual == 'atual'
    grupos = Grupo.objects.all()
    simulador.obter_dados_de_times(grupos, atual=atual)
    return render_to_response('classificacao.html', {
        'grupos': grupos, 'atual': atual, 'em_classificacao': True, 'titulo_da_pagina': "Classificação",
        'css_fundo': 'classificacao', 'pagina_atual': 'classificacao_real' if atual else 'classificacao_simulada',
    })


def classificacao_atual(request):
    grupos = Grupo.objects.all()
    simulador.obter_dados_de_times(grupos, atual=True)
    return render_to_response('classificacao.html', {'grupos': grupos, 'atual': True})


def chaves(request):
    fases = Fase.objects.all().exclude(slug='classificacao')
    for fase in fases:
        simulador.reordena_partidas_para_chave(fase)
    return render_to_response("chaves.html", {
        'rodadas': fases, 'index': index, 'chaves': True,
        'css_fundo': 'chaves', 'pagina_atual': 'chaves', 'titulo_da_pagina': "Chaves"
    })


def mostra_rodada(request, slug):
    return rodada(request, slug)


def rodada(request, slug, template='partidas.html', inclui_partida_em_andamento=False, titulo_da_pagina="Inicial"):
    grupos = Grupo.objects.all()
    partidas_em_andamento = simulador.obter_partidas_em_andamento()
    # for partida in partidas_em_andamento:
    #     simulador.atualiza_informacoes_de_partida_em_andamento(partida)
    #     partida.save()

    partidas = Partida.objects.filter(fase__slug=slug)
    # simulador.obter_times_de_partidas(partidas)

    titulos = {
        'oitavas': 'Oitavas'
    }

    if slug in titulos:
        titulo_da_pagina = titulos[slug]

    return render_to_response(
        template,
        {
            'partidas': partidas,
            'grupos': grupos,
            'titulo_da_pagina': titulo_da_pagina,
            'css_fundo': slug,
            'pagina_atual': slug
        }
    )


def registra_palpite(request):
    json = request.POST.get('json', '') == 'json'
    chaves = request.POST.get('chaves', '') == 'chaves'
    partida_id = request.POST['partida_id']

    palpite_time_1, palpite_time_2 = _obtem_palpites(request)

    partida = Partida.objects.get(id=partida_id)
    if partida.em_andamento():
        return HttpResponseRedirect('/rodada/%s' % partida.fase.slug)

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

    return HttpResponseRedirect('/rodada/%s' % partida.fase.slug)


def _obtem_palpites(request):
    try:
        palpite_time_1 = int(request.POST['time_1'])
        if palpite_time_1 < 0: palpite_time_1 = 0
    except ValueError:
        palpite_time_1 = 0
    try:
        palpite_time_2 = int(request.POST['time_2'])
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