#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mox import *
from nose.tools import assert_equals
import django
from copa_do_mundo.tabela import views

class FakeModel():
    def __init__(self, nome):
        self.nome = nome
    def __repr__(self):
        return self.nome

def test_obtem_lista_de_grupos():
    mox = Mox()
    mox.StubOutWithMock(views, 'simulador')
    mox.StubOutWithMock(views, 'render_to_response')
    request_mock = mox.CreateMockAnything()
    
    views.Grupo = mox.CreateMockAnything()
    views.Grupo.objects = mox.CreateMockAnything()
    grupo1 = FakeModel('grupo 1')
    grupo2 = FakeModel('grupo 2')
    grupos = [grupo1, grupo2]

    views.Grupo.objects.all().AndReturn(grupos)
    views.simulador.obter_dados_de_times(grupos)
    
    render_to_response = views.render_to_response
    views.render_to_response = mox.CreateMockAnything()
    views.render_to_response.__call__('grupos.html', {'grupos': grupos, 'atual': False})

    mox.ReplayAll()
    try:
        views.grupos(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
    
def test_obtem_lista_de_partidas():
    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, 're')
    mox.StubOutWithMock(views, 'render_to_response')
    mox.StubOutWithMock(views, 'simulador')
    mox.StubOutWithMock(views, '_obter_rodadas')

    request_mock = mox.CreateMockAnything()

    partida11 = FakeModel('Partida 1 da rodada 1')
    partida12 = FakeModel('Partida 1 da rodada 2')

    rodadas = [
        {'id': 'rodada_1', 'nome': '1ª Rodada', 'partidas': [partida11, partida12], 'index': 0}, 
        {'id': 'rodada_2', 'nome': '2ª Rodada', 'partidas': [partida11, partida12], 'index': 1}, 
        {'id': 'rodada_3', 'nome': '3ª Rodada', 'partidas': [partida11, partida12], 'index': 2},
        {'id': 'oitavas', 'nome': 'Oitavas', 'partidas': [partida11, partida12], 'index': 3},
        {'id': 'quartas', 'nome': 'Quartas', 'partidas': [partida11, partida12], 'index': 4},
        {'id': 'semifinais', 'nome': 'Semifinais', 'partidas': [partida11, partida12], 'index': 5},
        {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'partidas': [partida11, partida12], 'index': 6},
        {'id': 'final', 'nome': 'Final', 'partidas': [partida11, partida12], 'index': 7}
    ]
    
    views._obter_rodadas().AndReturn(rodadas)
    views.Partida.objects = mox.CreateMockAnything()

    count = 0
    for rodada in rodadas:
        views.Partida.objects.filter(rodada__exact=rodada['id']).AndReturn([partida11, partida12])
        retorna = count % 2 == 0
        views.re.match('[1-3]', rodada['nome']).AndReturn(retorna)
        count += 1
        if not retorna:
            views.simulador.obter_times_de_partidas(rodada['partidas'])
        else:
            for partida in rodada['partidas']:
                views.simulador.atualiza_informacoes_de_partida_em_andamento(partida)
                partida.save = lambda : None
                
    views.render_to_response.__call__('partidas.html', {'rodadas': rodadas, 'index': 0, 'chaves': False})

    mox.ReplayAll()
    try:
        views.partidas(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_registra_palpite_com_gols_validos_e_votos_zero():
    
    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')
    request_mock = mox.CreateMockAnything()
    
    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}
    views._obtem_palpites(request_mock).AndReturn((2, 1))
    
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 0
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()
    
    views.HttpResponseRedirect('/partidas.html')
    
    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 1)
    assert_equals(partida.palpites_time_1, 2)
    assert_equals(partida.palpites_time_2, 1)

    
def test_registra_palpite_com_gols_validos_e_votos_nulo():

    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')
    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

    views._obtem_palpites(request_mock).AndReturn((2, 1))

    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = None
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 1)
    assert_equals(partida.palpites_time_1, 2)
    assert_equals(partida.palpites_time_2, 1)

def test_registra_palpite_com_gols_validos_e_com_votos():

    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')

    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}
    views._obtem_palpites(request_mock).AndReturn((2, 1))

    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 6)
    assert_equals(partida.palpites_time_2, 7)

def test_registra_palpite_com_gols_invalidos_considera_zero():

    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')

    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': 'a', 'palpiteTime2': ''}

    views._obtem_palpites(request_mock).AndReturn((0, 0))

    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 4)
    assert_equals(partida.palpites_time_2, 6)


def test_registra_palpite_com_gols_negativos_considera_zero():
    
    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')

    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '-3', 'palpiteTime2': '-1'}

    views._obtem_palpites(request_mock).AndReturn((0, 0))

    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 4)
    assert_equals(partida.palpites_time_2, 6)


def test_registra_palpite_com_retorno_json():

    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, '_obtem_palpites')

    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'json': 'json', 'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

    views._obtem_palpites(request_mock).AndReturn((2, 1))
    
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.id = 1
    partida.media_palpites_time_1 = lambda : 2
    partida.media_palpites_time_2 = lambda : 1
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.em_andamento = lambda : False
    partida.save()

    views.HttpResponse('{"partida_id": "partida_1", "gols_time_1": 2, "gols_time_2": 1, "votos": 3}', mimetype="text/json")

    mox.ReplayAll()
    try:
        views.registra_palpite(request_mock)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 6)
    assert_equals(partida.palpites_time_2, 7)

def test_obtem_dados_de_rodada_pelo_id():
    mox = Mox()
    mox.StubOutWithMock(views, 'Partida')
    mox.StubOutWithMock(views, 're')
    mox.StubOutWithMock(views, 'render_to_response')
    mox.StubOutWithMock(views, '_obter_rodadas')

    request_mock = mox.CreateMockAnything()

    partida11 = FakeModel('Partida 1 da rodada 1')
    partida12 = FakeModel('Partida 1 da rodada 2')

    rodadas = [
        {'id': 'rodada_1', 'nome': '1ª Rodada', 'index': 0}, 
        {'id': 'rodada_2', 'nome': '2ª Rodada', 'index': 1}, 
        {'id': 'rodada_3', 'nome': '3ª Rodada', 'index': 2},
        {'id': 'oitavas', 'nome': 'Oitavas', 'index': 3},
        {'id': 'quartas', 'nome': 'Quartas', 'index': 4},
        {'id': 'semifinais', 'nome': 'Semifinais', 'index': 5},
        {'id': 'terceiro_lugar', 'nome': 'Terceiro Lugar', 'index': 6},
        {'id': 'final', 'nome': 'Final', 'index': 7, 'partidas': [partida11, partida12]}
    ]

    views._obter_rodadas.__call__().AndReturn(rodadas)

    views.Partida.objects = mox.CreateMockAnything()
    views.Partida.objects.filter(rodada__exact='final').AndReturn([partida11, partida12])
    views.re.match('[1-3]', 'Final').AndReturn('AlgumaCoisa')
    views.render_to_response.__call__('partidas.html', {'rodadas': rodadas, 'rodada_id': 'final', 'index': 7})

    mox.ReplayAll()
    try:
        views.rodada(request_mock, 'final')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
    
