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
    
    views.Time = mox.CreateMockAnything()
    views.Time.objects = mox.CreateMockAnything()

    time1 = FakeModel('time 1 do grupo 1')
    time2 = FakeModel('time 2 do grupo 1')
    time3 = FakeModel('time 1 do grupo 2')
    time4 = FakeModel('time 2 do grupo 2')

    times1 = [time1, time2]
    times2 = [time3, time4]
    views.Time.objects.filter(grupo__nome__exact=grupo1.nome).AndReturn(times1)
    views.Time.objects.filter(grupo__nome__exact=grupo2.nome).AndReturn(times2)
    django.shortcuts = mox.CreateMockAnything()

    views.render_to_response('grupos.html', {'grupos': grupos})
    mox.ReplayAll()

    views.grupos(request_mock)

    mox.VerifyAll()

    assert_equals(grupos[0].times[0].nome, 'time 1 do grupo 1')
    assert_equals(grupos[1].times[0].nome, 'time 1 do grupo 2')
    
def test_obtem_lista_de_partidas():
    mox = Mox()
    request_mock = mox.CreateMockAnything()

    partida11 = FakeModel('Partida 1 da rodada 1')
    partida12 = FakeModel('Partida 1 da rodada 2')
    partida22 = FakeModel('Partida 2 da rodada 2')
    partida13 = FakeModel('Partida 1 da rodada 3')
    partida23 = FakeModel('Partida 2 da rodada 3')
    partida33 = FakeModel('Partida 3 da rodada 3')

    rodadas = [
        {'id': 'rodada_1', 'nome': '1 Rodada', 'partidas': [partida11, partida12]}, 
        {'id': 'rodada_2', 'nome': '2 Rodada', 'partidas': [partida22]}, 
        {'id': 'rodada_3', 'nome': '3 Rodada', 'partidas': [partida13, partida23, partida33]}
    ]
    
    views.Partida = mox.CreateMockAnything()
    views.Partida.objects = mox.CreateMockAnything()

    views.Partida.objects.filter(rodada__exact='1 Rodada').AndReturn([partida11, partida12])
    views.Partida.objects.filter(rodada__exact='2 Rodada').AndReturn([partida22])
    views.Partida.objects.filter(rodada__exact='3 Rodada').AndReturn([partida13, partida23, partida33])
    
    views.render_to_response('partidas.html', {'rodadas': rodadas})
    mox.ReplayAll()

    views.partidas(request_mock)

    mox.VerifyAll()

def test_registra_palpite_com_gols_validos_e_votos_zero():
    
    mox = Mox()
    request_mock = mox.CreateMockAnything()
    
    request_mock.GET = {'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}
    
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

    request_mock.GET = {'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

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

    request_mock.GET = {'partida_id': '1', 'palpiteTime1': '2', 'palpiteTime2': '1'}

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

    request_mock.GET = {'partida_id': '1', 'palpiteTime1': 'a', 'palpiteTime2': ''}

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

    request_mock.GET = {'partida_id': '1', 'palpiteTime1': '-3', 'palpiteTime2': '-1'}

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
