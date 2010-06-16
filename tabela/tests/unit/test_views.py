#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mox import *
from nose.tools import assert_equals
import django
from copa_do_mundo.tabela import views

class FakeModel():
    def __init__(self, nome):
        self.nome = nome

def test_obtem_lista_de_grupos():
    mox = Mox()
    request_mock = mox.CreateMockAnything()
    
    views.Grupo = mox.CreateMockAnything()
    views.Grupo.objects = mox.CreateMockAnything()
    grupo1 = FakeModel('grupo 1')
    grupo2 = FakeModel('grupo 2')
    grupos = [grupo1, grupo2]

    views.Grupo.objects.all().AndReturn(grupos)
    simulador = views.simulador
    views.simulador = mox.CreateMockAnything()
    views.simulador.obter_dados_de_times(grupos)
    
    render_to_response = views.render_to_response
    views.render_to_response = mox.CreateMockAnything()
    views.render_to_response.__call__('grupos.html', {'grupos': grupos})
    mox.ReplayAll()

    views.grupos(request_mock)

    mox.VerifyAll()

    views.simulador = simulador
    views.render_to_response = render_to_response
    
def test_obtem_lista_de_partidas():

    mox = Mox()
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
    
    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()
    simulador = views.simulador
    views.simulador = mox.CreateMockAnything()
    
    views.re = mox.CreateMockAnything()
    count = 0
    for rodada in rodadas:
        views.Partida.objects.filter(rodada__exact=rodada['id']).AndReturn([partida11, partida12])
        retorna = count % 2 == 0
        views.re.match('[1-3]', rodada['nome']).AndReturn(retorna)
        count += 1
        if not retorna:
            views.simulador.obter_times_de_partidas(rodada['partidas'])

    render_to_response = views.render_to_response
    views.render_to_response = mox.CreateMockAnything()
    views.render_to_response.__call__('partidas.html', {'rodadas': rodadas, 'index': 1})
    mox.ReplayAll()

    views.partidas(request_mock)

    mox.VerifyAll()
    views.simulador = simulador
    views.render_to_response = render_to_response

def test_registra_palpite_com_gols_validos_e_votos_zero():
    
    mox = Mox()
    request_mock = mox.CreateMockAnything()
    
    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}
    
    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 0
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.save()
    
    views.HttpResponseRedirect('/partidas.html')
    
    mox.ReplayAll()

    views.registra_palpite(request_mock)

    mox.VerifyAll()

    assert_equals(partida.votos, 1)
    assert_equals(partida.palpites_time_1, 2)
    assert_equals(partida.palpites_time_2, 1)

    
def test_registra_palpite_com_gols_validos_e_votos_nulo():

    mox = Mox()
    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = None
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()

    views.registra_palpite(request_mock)

    mox.VerifyAll()

    assert_equals(partida.votos, 1)
    assert_equals(partida.palpites_time_1, 2)
    assert_equals(partida.palpites_time_2, 1)

def test_registra_palpite_com_gols_validos_e_com_votos():

    mox = Mox()
    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()

    views.registra_palpite(request_mock)

    mox.VerifyAll()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 6)
    assert_equals(partida.palpites_time_2, 7)

def test_registra_palpite_com_gols_invalidos_considera_zero():

    mox = Mox()
    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': 'a', 'palpiteTime2': ''}

    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()

    views.registra_palpite(request_mock)

    mox.VerifyAll()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 4)
    assert_equals(partida.palpites_time_2, 6)


def test_registra_palpite_com_gols_negativos_considera_zero():
    
    mox = Mox()
    request_mock = mox.CreateMockAnything()

    request_mock.GET = {'rodada_id': 'rodada_1', 'partida_id': '1', 'palpiteTime1': '-3', 'palpiteTime2': '-1'}

    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    partida = mox.CreateMockAnything()
    partida.votos = 2
    partida.palpites_time_1 = 4
    partida.palpites_time_2 = 6
    views.Partida.objects.get(id='1').AndReturn(partida)
    partida.save()

    views.HttpResponseRedirect('/partidas.html')

    mox.ReplayAll()

    views.registra_palpite(request_mock)

    mox.VerifyAll()

    assert_equals(partida.votos, 3)
    assert_equals(partida.palpites_time_1, 4)
    assert_equals(partida.palpites_time_2, 6)
