#!/usr/bin/env python
# encoding: utf-8
import json
from urlparse import unquote
from django.conf import settings

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from tabela.models import Grupo, Partida, Fase


def criar_contexto(request, titulo_da_pagina, pagina_atual, css_fundo, partidas=None):
    grupos = Grupo.objects.all()
    partidas_cookie = unquote(request.COOKIES.get("partidas", ""))
    partidas_votadas = []
    if partidas_cookie:
        partidas_votadas = json.loads(partidas_cookie)

    proximas_partidas = [
        partida for partida in
        Partida.objects.filter(realizada=False).order_by('data')[:6] if not partida.em_andamento()
    ]
    partidas_em_andamento = [
        partida for partida in
        Partida.objects.filter(realizada=False).order_by('data')[:6] if partida.em_andamento()
    ]
    contexto = {
        'grupos': grupos, 'grupos_classificando': grupos, 'pagina_atual': pagina_atual, 'partidas': partidas,
        'css_fundo': css_fundo, 'titulo_da_pagina': titulo_da_pagina, 'partidas_votadas': partidas_votadas,
        'partidas_atuais': partidas_em_andamento, 'proximas_partidas': proximas_partidas[:4]
    }
    contexto.update(csrf(request))
    return contexto


def index(request):
    return render_to_response('index.html', criar_contexto(request, "Inicial", "inicial", "inicial"))


def partidas_de_grupo(request, nome):
    grupo = Grupo.objects.get(nome=nome)
    partidas_do_grupo = grupo.partidas_do_grupo_na_fase('classificacao')
    contexto = criar_contexto(request, "Grupo {}".format(grupo.nome), grupo.nome, 'grupos', partidas_do_grupo)
    contexto.update({'em_grupos': True})
    return render_to_response('grupo.html', contexto)


def classificacao(request, atual=None):
    atual = atual == 'atual'
    contexto = criar_contexto(request, "Classificação", 'classificacao_real' if atual else 'classificacao_simulada', 'classificacao')
    # simulador.obter_dados_de_times(contexto['grupos'], atual=atual)
    contexto.update({'em_classificacao': True, 'atual': atual})
    return render_to_response('classificacao.html', contexto)


def mostra_rodada(request, slug):
    fase = Fase.objects.get(slug=slug)
    partidas = Partida.objects.filter(fase=fase)
    contexto = criar_contexto(request, fase.nome, slug, slug, partidas)
    return render_to_response('partidas.html', contexto)


def registra_palpite(request):
    partida_id = request.POST.get('partida_id')
    palpite_time_1, palpite_time_2 = _obtem_palpites(request)
    partida = Partida.objects.get(id=partida_id)
    if partida.em_andamento():
        return redirect('rodada', partida.fase.slug)
    partida.registra_palpite(palpite_time_1, palpite_time_2)
    resultado = {
        "partida_id": "partida_{}".format(partida.id),
        "gols_time_1": partida.media_palpites_time_1(),
        "gols_time_2": partida.media_palpites_time_2(),
        "votos": partida.votos
    }
    return HttpResponse(json.dumps(resultado), mimetype="application/json")


def _obtem_palpites(request):
    try:
        palpite_time_1 = int(request.POST.get('time_1'))
        if palpite_time_1 < 0:
            palpite_time_1 = 0
    except ValueError:
        palpite_time_1 = 0
    try:
        palpite_time_2 = int(request.POST.get('time_2'))
        if palpite_time_2 < 0:
            palpite_time_2 = 0
    except ValueError:
        palpite_time_2 = 0

    if palpite_time_1 > 9:
        palpite_time_1 = 0

    if palpite_time_2 > 9:
        palpite_time_2 = 0

    return palpite_time_1, palpite_time_2


def publica_no_facebook(request):
    from pip._vendor import requests
    message = request.GET.get("message", None)
    if not message:
        message = "Made by my Django App"
    facebook_post = {
        "message": message,
        "link": "http://g1.globo.com/"
    }
    resultado = requests.post("{}/{}/feed?access_token={}".format(settings.FACEBOOK_GRAPH_API, settings.FACEBOOK_PAGE_ID, settings.FACEBOOK_PAGE_ACCESS_TOKEN), data=facebook_post)
    return HttpResponse(resultado.text, mimetype="application/json")


def obtem_access_token(request):
    from pip._vendor import requests
    url = "{}/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}"
    app_id = ""
    app_scret = ""
    temporary_access_token = ""
    resultado = requests.get(url.format(settings.FACEBOOK_GRAPH_API, app_id, app_scret, temporary_access_token))
    return HttpResponse(resultado.text, mimetype="application/json")