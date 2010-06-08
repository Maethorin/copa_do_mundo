#!/usr/bin/env python
# encoding: utf-8

from mox import *
from nose.tools import assert_equals
from copa_do_mundo.tabela import simulador

class FakeModel():
    def __init__(self, nome):
        self.nome = nome

def test_obtem_times_de_partida_de_oitavas():
    
    mox = Mox()

    time1 = FakeModel('time1')
    time2 = FakeModel('time2')
    regra = '1Ax2B'
    grupos = ['A', 'B']
    grupo1 = grupos[0]
    grupo2 = grupos[1]
    classificacoes = ['1', '2']
    simulador.parser_regra = mox.CreateMockAnything()
    simulador.parser_regra.obtem_grupos_de_regra(regra).AndReturn(grupos)
    simulador.parser_regra.obtem_classificacoes_de_regra(regra).AndReturn(classificacoes)
    obtem_time_do_grupo_na_classificacao = simulador.obtem_time_do_grupo_na_classificacao
    simulador.obtem_time_do_grupo_na_classificacao = mox.CreateMockAnything()    
    simulador.obtem_time_do_grupo_na_classificacao.__call__(grupos[0], classificacoes[0]).AndReturn(time1)
    simulador.obtem_time_do_grupo_na_classificacao.__call__(grupos[1], classificacoes[1]).AndReturn(time2)

    mox.ReplayAll()

    timeA, timeB = simulador.obtem_times_de_partida_de_oitavas(regra)

    mox.VerifyAll()
    
    assert_equals(time1, timeA)
    assert_equals(time2, timeB)
    
    simulador.obtem_time_do_grupo_na_classificacao = obtem_time_do_grupo_na_classificacao

def test_obtem_time_do_grupo_em_classificacao_para_primeira_fase():
    mox = Mox()

    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 0
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 0
    times = [time1, time2]

    simulador.Time = mox.CreateMockAnything()
    simulador.Time.objects = mox.CreateMockAnything()
    simulador.Time.objects.filter(grupo__nome__exact='A').AndReturn(times)
    simulador.Partida = mox.CreateMockAnything()
    simulador.Partida.objects = mox.CreateMockAnything()
    simulador.Q = mox.CreateMockAnything()
    obter_vitorioso_na_partida = simulador.obter_vitorioso_na_partida
    normalizar_lista_com_saldo_de_gols = simulador.normalizar_lista_com_saldo_de_gols
    simulador.obter_vitorioso_na_partida = mox.CreateMockAnything()
    simulador.normalizar_lista_com_saldo_de_gols = mox.CreateMockAnything()

    partida1 = FakeModel('partida1')
    partida1.vitorioso = time1
    partida2 = FakeModel('partida2')
    partida2.vitorioso = None
    partidas = [partida1, partida2]

    for time in times:
        simulador.Q.__call__(time_1__id__exact=time.id).AndReturn(True)
        simulador.Q.__call__(time_2__id__exact=time.id).AndReturn(True)
        simulador.Partida.objects.filter(True | True).AndReturn(partidas)
        for partida in partidas:
            simulador.obter_vitorioso_na_partida.__call__(partida).AndReturn(partida.vitorioso)

    simulador.normalizar_lista_com_saldo_de_gols.__call__(times)

    mox.ReplayAll()

    retorno = simulador.obtem_time_do_grupo_na_classificacao('A', 1)

    mox.VerifyAll()
    
    assert_equals(retorno, time1)
    simulador.obter_vitorioso_na_partida = obter_vitorioso_na_partida
    simulador.normalizar_lista_com_saldo_de_gols = normalizar_lista_com_saldo_de_gols

def test_obter_vitorioso_na_partida_realizada():
    mox = Mox()

    partida = FakeModel('partida')
    partida.realizada = True
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 2
    analiza_resultado = simulador.analiza_resultado
    simulador.analiza_resultado = mox.CreateMockAnything()
    
    simulador.analiza_resultado.__call__(3, 2, partida).AndReturn(partida.time_1)
    mox.ReplayAll()

    vitorioso = simulador.obter_vitorioso_na_partida(partida)

    mox.VerifyAll()
    
    assert_equals(vitorioso, partida.time_1)
    
    simulador.analiza_resultado = analiza_resultado

def test_obter_vitorioso_na_partida_nao_realizada():
    mox = Mox()

    partida = FakeModel('partida')
    partida.realizada = False
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.palpites_time_1 = 1
    partida.palpites_time_2 = 2
    analiza_resultado = simulador.analiza_resultado
    simulador.analiza_resultado = mox.CreateMockAnything()

    simulador.analiza_resultado.__call__(1, 2, partida).AndReturn(partida.time_2)
    mox.ReplayAll()

    vitorioso = simulador.obter_vitorioso_na_partida(partida)

    mox.VerifyAll()

    assert_equals(vitorioso, partida.time_2)
    
    simulador.analiza_resultado = analiza_resultado

def test_analiza_resultado_retorna_none_quando_empate():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 3

    time = simulador.analiza_resultado(partida.gols_time_1, partida.gols_time_2, partida)
    
    assert_equals(time, None)

def test_analiza_resultado_retorna_time_1():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 2

    time = simulador.analiza_resultado(partida.gols_time_1, partida.gols_time_2, partida)

    assert_equals(time, partida.time_1)

def test_analiza_resultado_retorna_time_2():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 2
    partida.gols_time_2 = 3

    time = simulador.analiza_resultado(partida.gols_time_1, partida.gols_time_2, partida)

    assert_equals(time, partida.time_2)

def test_normalizar_lista_com_saldo_de_gols_quando_nao_ha_empate_nada_faz():
    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 4
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 2
    time3 = FakeModel('time3')
    time3.id = 3
    time3.pontos = 1
    times = [time1, time2, time3]

    simulador.normalizar_lista_com_saldo_de_gols(times)
    
    assert_equals(times[0], time1)
    assert_equals(times[1], time2)
    assert_equals(times[2], time3)

def test_normalizar_lista_com_saldo_de_gols_recupera_saldo_quando_ha_empate():
    mox = Mox()
    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 4
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 2
    time3 = FakeModel('time3')
    time3.id = 3
    time3.pontos = 2
    times = [time1, time2, time3]
    
    adiciona_time_a_lista = simulador.adiciona_time_a_lista
    obter_saldos_de_gols = simulador.obter_saldos_de_gols
    simulador.adiciona_time_a_lista = mox.CreateMockAnything()
    simulador.adiciona_time_a_lista.__call__([], time2)
    simulador.adiciona_time_a_lista.__call__([], time3)
    simulador.obter_saldos_de_gols = mox.CreateMockAnything()
    simulador.obter_saldos_de_gols.__call__([])
    
    mox.ReplayAll()
    simulador.normalizar_lista_com_saldo_de_gols(times)
    mox.VerifyAll()
    simulador.adiciona_time_a_lista = adiciona_time_a_lista
    simulador.obter_saldos_de_gols = obter_saldos_de_gols
