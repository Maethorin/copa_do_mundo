#!/usr/bin/env python
# encoding: utf-8
import json
from urlparse import unquote
from django.conf import settings

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from tabela.models import Grupo, Partida, Fase


class OpenGraph(object):
    def __init__(self, title, site_name, url, description, image=None, content_type="article"):
        self.app_id = settings.FACEBOOK_APP_ID
        self.title = title
        self.site_name = site_name
        self.url = url
        self.description = description
        self.image = image or "{}{}img/logo-simulacopa.png".format(settings.BASE_URL, settings.STATIC_URL)
        self.type = content_type


def criar_contexto(request, titulo_da_pagina, pagina_atual, css_fundo, og, partidas=None):
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
        'partidas_atuais': partidas_em_andamento, 'proximas_partidas': proximas_partidas[:4],
        'og': og
    }
    contexto.update(csrf(request))
    return contexto


def index(request):
    og = OpenGraph(
        "Como funciona o Simulador",
        "Simulador da Copa do Mundo",
        settings.BASE_URL,
        u"Regras de como funciona o Simulador da Copa do Mundo. É, basicamente, o resultado da média dos palpites. Veja mais."
    )
    return render_to_response('index.html', criar_contexto(request, "Inicial", "inicial", "inicial", og))


def agenda(request):
    og = OpenGraph(
        "Agenda dos jogos da copa",
        "Simulador da Copa do Mundo",
        "{}{}".format(settings.BASE_URL, reverse('agenda')),
        u"Lista dos jogos em andamento e dos próximos jogos. Mostra o placar atual do jogo em andamento. O quatro próximos jogos são exibidos."
    )
    return render_to_response('agenda.html', criar_contexto(request, "Agenda", "agenda", "agenda", og))


def partidas_de_grupo(request, nome):
    grupo = Grupo.objects.get(nome=nome)
    og = OpenGraph(
        u"Jogos de classificação do Grupo {}".format(grupo.nome),
        "Simulador da Copa do Mundo",
        "{}{}".format(settings.BASE_URL, reverse('grupo', args=[grupo.nome])),
        u"Jogos de classificação do Grupo {} com os campos para os palpites de placar no jogo. Só poderá ser dado um palpite por jogo. Os jogos estão agrupados por rodada.".format(grupo.nome)
    )
    partidas_do_grupo = grupo.partidas_do_grupo_na_fase('classificacao')
    contexto = criar_contexto(request, "Grupo {}".format(grupo.nome), grupo.nome, 'grupos', og, partidas=partidas_do_grupo)
    contexto.update({'em_grupos': True})
    return render_to_response('grupo.html', contexto)


def classificacao(request, atual=None):
    atual = atual == 'atual'
    url = "{}{}".format(settings.BASE_URL, reverse('classificacao'))
    if atual:
        url = "{}{}".format(settings.BASE_URL, reverse('classificacao', args=['atual']))
    og = OpenGraph(
        u"Tabela de classificação",
        "Simulador da Copa do Mundo",
        url,
        "Tabela contento a classificação {} da 1ª fase da Copa. A tabela está organizada por grupo e tem as informação de pontos, jogos disputados, vitórias, empates, derrotas, gols pró, gols contra, saldo de gols e aproveitamento".format(('real' if atual else 'simulada'))
    )
    contexto = criar_contexto(request, "Classificação", 'classificacao_real' if atual else 'classificacao_simulada', 'classificacao', og)
    contexto.update({'em_classificacao': True, 'atual': atual})
    return render_to_response('classificacao.html', contexto)


def mostra_rodada(request, slug):
    fase = Fase.objects.get(slug=slug)
    og = OpenGraph(
        u"Jogos de {}".format(fase.nome),
        "Simulador da Copa do Mundo",
        "{}{}".format(settings.BASE_URL, reverse('rodada', args=[fase.slug])),
        u"Jogos de {} com os campos para os palpites de placar no jogo. Só poderá ser dado um palpite por jogo. Os jogos estão ordenados por data".format(fase.nome)
    )
    partidas = Partida.objects.filter(fase=fase)
    contexto = criar_contexto(request, fase.nome, slug, slug, og, partidas=partidas)
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
