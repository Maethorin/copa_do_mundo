#!/usr/bin/env python
# encoding: utf-8

from mox import *
from nose.tools import assert_equals
from copa_do_mundo.tabela import simulador

class FakeModel():
    def __init__(self, nome):
        self.nome = nome
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_feitos = 0
        self.gols_tomados = 0
    
    def __repr__(self):
        return self.nome

def test_obter_time_de_partidas_com_partidas_de_oitavas():

    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')

    time1 = FakeModel('time1')
    time2 = FakeModel('time2')
    regra = 'O43x44'

    partida1 = FakeModel('partida1')
    partida1.vitorioso = time1
    partida1.rodada = 'oitavas'
    partida1.regra_para_times = regra
    
    partida2 = FakeModel('partida2')
    partida2.vitorioso = None
    partida2.rodada = 'oitavas'
    partida2.regra_para_times = regra

    partidas = [partida1, partida2]
    
    simulador.obtem_times_de_partida_de_oitavas.__call__(regra).AndReturn([time1, time2])
    simulador.obtem_times_de_partida_de_oitavas.__call__(regra).AndReturn([time2, time1])

    mox.ReplayAll()
    try:
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obter_time_de_partidas_com_partidas_de_outras_fases():

    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_outras_fases')

    time1 = FakeModel('time1')
    time2 = FakeModel('time2')
    regra = 'Q43x44'

    partida1 = FakeModel('partida1')
    partida1.vitorioso = time1
    partida1.rodada = 'quartas'
    partida1.regra_para_times = regra

    partida2 = FakeModel('partida2')
    partida2.vitorioso = None
    partida2.rodada = 'quartas'
    partida2.regra_para_times = regra

    partidas = [partida1, partida2]

    simulador.obtem_times_de_partida_de_outras_fases.__call__(regra).AndReturn([time1, time2])
    simulador.obtem_times_de_partida_de_outras_fases.__call__(regra).AndReturn([time2, time1])

    mox.ReplayAll()
    try:
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obter_time_de_partidas_com_partidas_de_outras_fases_e_de_oitavas():

    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_outras_fases')
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')

    time1 = FakeModel('time1')
    time2 = FakeModel('time2')
    regra = 'Q43x44'

    partida1 = FakeModel('partida1')
    partida1.vitorioso = time1
    partida1.rodada = 'quartas'
    partida1.regra_para_times = regra

    partida2 = FakeModel('partida2')
    partida2.vitorioso = None
    partida2.rodada = 'oitavas'
    partida2.regra_para_times = regra

    partidas = [partida1, partida2]

    simulador.obtem_times_de_partida_de_outras_fases.__call__(regra).AndReturn([time1, time2])
    simulador.obtem_times_de_partida_de_oitavas.__call__(regra).AndReturn([time2, time1])

    mox.ReplayAll()
    try:
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_times_de_partida_de_oitavas():

    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
    mox.StubOutWithMock(simulador, 'parser_regra')

    time1 = FakeModel('time1')
    time2 = FakeModel('time2')
    regra = '1Ax2B'
    grupos = ['A', 'B']
    grupo1 = grupos[0]
    grupo2 = grupos[1]
    classificacoes = ['1', '2']

    simulador.parser_regra.obtem_grupos_de_regra(regra).AndReturn(grupos)
    simulador.parser_regra.obtem_classificacoes_de_regra(regra).AndReturn(classificacoes)

    simulador.obtem_time_do_grupo_na_classificacao.__call__(grupos[0], classificacoes[0]).AndReturn(time1)
    simulador.obtem_time_do_grupo_na_classificacao.__call__(grupos[1], classificacoes[1]).AndReturn(time2)

    mox.ReplayAll()
    try:
        timeA, timeB = simulador.obtem_times_de_partida_de_oitavas(regra)
        assert_equals(time1, timeA)
        assert_equals(time2, timeB)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_times_de_partida_de_outras_fases_com_regra_de_oitavas():
    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
    mox.StubOutWithMock(simulador, 'parser_regra')
    mox.StubOutWithMock(simulador, 'Partida')
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
    mox.StubOutWithMock(simulador, 'obter_time_na_partida')

    regra = 'O53x54'
    simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
    simulador.Partida.objects = mox.CreateMockAnything()
    partida1 = FakeModel('partida 1')
    partida1.rodada = 'oitavas'
    partida1.regra_para_times = 'O56x57'
    partida2 = FakeModel('partida 2')
    partida2.regra_para_times = 'O51x52'

    simulador.Partida.objects.get(id='53').AndReturn(partida1)
    simulador.Partida.objects.get(id='54').AndReturn(partida2)

    time1 = FakeModel('time 1')
    time2 = FakeModel('time 2')
    simulador.obtem_times_de_partida_de_oitavas('O56x57').AndReturn((time1, time2))
    simulador.obtem_times_de_partida_de_oitavas('O51x52').AndReturn((time2, time1))

    simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

    mox.ReplayAll()
    try:
        timeA, timeB = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, timeA)
        assert_equals(time2, timeB)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_times_de_partida_de_outras_fases_com_regra_de_outras_fases():
    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
    mox.StubOutWithMock(simulador, 'parser_regra')
    mox.StubOutWithMock(simulador, 'Partida')
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
    mox.StubOutWithMock(simulador, 'obter_time_na_partida')

    regra = 'O53x54'
    simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
    simulador.Partida.objects = mox.CreateMockAnything()
    partida1 = FakeModel('partida 1')
    partida1.rodada = 'quartas'
    partida1.regra_para_times = 'Q56x57'
    partida2 = FakeModel('partida 2')
    partida2.regra_para_times = 'Q51x52'

    partida3 = FakeModel('partida 3')
    partida3.rodada = 'oitavas'
    partida3.regra_para_times = 'O53x54'
    partida4 = FakeModel('partida 4')
    partida4.regra_para_times = 'O58x59'

    time1 = FakeModel('time 1')
    time2 = FakeModel('time 2')

    simulador.Partida.objects.get(id='53').AndReturn(partida1)
    simulador.Partida.objects.get(id='54').AndReturn(partida2)

    simulador.parser_regra.eh_disputa_de_terceiro_lugar(regra).AndReturn(False)

    simulador.parser_regra.obtem_ids_de_partida_de_regra(partida1.regra_para_times).AndReturn(['56', '57'])
    simulador.Partida.objects.get(id='56').AndReturn(partida3)
    simulador.Partida.objects.get(id='57').AndReturn(partida4)

    simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
    simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

    simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

    simulador.parser_regra.obtem_ids_de_partida_de_regra(partida2.regra_para_times).AndReturn(['51', '52'])
    simulador.Partida.objects.get(id='51').AndReturn(partida3)
    simulador.Partida.objects.get(id='52').AndReturn(partida4)

    simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
    simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

    simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

    simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

    mox.ReplayAll()
    try:
        timeA, timeB = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, timeA)
        assert_equals(time2, timeB)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_times_de_partida_de_disputa_de_terceiro_lugar():
    mox = Mox()
    mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
    mox.StubOutWithMock(simulador, 'parser_regra')
    mox.StubOutWithMock(simulador, 'Partida')
    mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
    mox.StubOutWithMock(simulador, 'obter_time_na_partida')

    regra = 'O53x54'
    simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
    simulador.Partida.objects = mox.CreateMockAnything()
    partida1 = FakeModel('partida 1')
    partida1.rodada = 'quartas'
    partida1.regra_para_times = 'Q56x57'
    partida2 = FakeModel('partida 2')
    partida2.regra_para_times = 'Q51x52'

    partida3 = FakeModel('partida 3')
    partida3.rodada = 'oitavas'
    partida3.regra_para_times = 'O53x54'
    partida4 = FakeModel('partida 4')
    partida4.regra_para_times = 'O58x59'

    time1 = FakeModel('time 1')
    time2 = FakeModel('time 2')

    simulador.Partida.objects.get(id='53').AndReturn(partida1)
    simulador.Partida.objects.get(id='54').AndReturn(partida2)

    simulador.parser_regra.eh_disputa_de_terceiro_lugar(regra).AndReturn(True)

    simulador.parser_regra.obtem_ids_de_partida_de_regra(partida1.regra_para_times).AndReturn(['56', '57'])
    simulador.Partida.objects.get(id='56').AndReturn(partida3)
    simulador.Partida.objects.get(id='57').AndReturn(partida4)

    simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
    simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

    simulador.obter_time_na_partida(partida3, True).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida4, True).AndReturn((time2, 2, 3))

    simulador.parser_regra.obtem_ids_de_partida_de_regra(partida2.regra_para_times).AndReturn(['51', '52'])
    simulador.Partida.objects.get(id='51').AndReturn(partida3)
    simulador.Partida.objects.get(id='52').AndReturn(partida4)

    simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
    simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

    simulador.obter_time_na_partida(partida3, True).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida4, True).AndReturn((time2, 2, 3))

    simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
    simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

    mox.ReplayAll()
    try:
        timeA, timeB = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, timeA)
        assert_equals(time2, timeB)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_time_do_grupo_na_classificacao():
    mox = Mox()

    classificacao = 1
    mox.StubOutWithMock(simulador, 'obtem_times_do_grupo_ordenados_por_classificacao')

    simulador.obtem_times_do_grupo_ordenados_por_classificacao.__call__('A').AndReturn(['timeA', 'timeB'])
    mox.ReplayAll()
    try:
        retorno = simulador.obtem_time_do_grupo_na_classificacao('A', 1)
        mox.VerifyAll()
        assert_equals(retorno, 'timeA')
    finally:
        mox.UnsetStubs()
    
def test_obtem_times_do_grupo_ordenados_por_classificacao():
    mox = Mox()

    mox.StubOutWithMock(simulador, 'normalizar_lista_com_saldo_de_gols')
    mox.StubOutWithMock(simulador, 'soma_gols_do_time')
    mox.StubOutWithMock(simulador, 'obter_time_na_partida')
    mox.StubOutWithMock(simulador, 'Time')
    mox.StubOutWithMock(simulador, 'Partida')
    mox.StubOutWithMock(simulador, 'Q')

    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 2
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 0
    times = [time1, time2]

    simulador.Time.objects = mox.CreateMockAnything()
    simulador.Time.objects.filter(grupo__nome__exact='A').AndReturn(times)
    simulador.Partida.objects = mox.CreateMockAnything()

    partida1 = FakeModel('partida1')
    partida1.vitorioso = time1
    partida1.time_1 = time1
    partida1.time_2 = time2
    
    partida2 = FakeModel('partida2')
    partida2.vitorioso = None
    partida2.time_1 = time1
    partida2.time_2 = time2

    partidas = [partida1, partida2]

    for time in times:
        simulador.Q.__call__(time_1__id__exact=time.id).AndReturn(True)
        simulador.Q.__call__(time_2__id__exact=time.id).AndReturn(True)
        simulador.Partida.objects.filter(True | True).AndReturn(partidas)
        for partida in partidas:
            simulador.obter_time_na_partida.__call__(partida).AndReturn((partida.vitorioso, 0, 0))
            simulador.soma_gols_do_time(time, 0, 0, partida.time_1.id)

    simulador.normalizar_lista_com_saldo_de_gols(times)
    mox.ReplayAll()
    try:
        retorno = simulador.obtem_times_do_grupo_ordenados_por_classificacao('A')
        assert_equals(retorno, [time1, time2])
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obter_vitorioso_na_partida_realizada():
    mox = Mox()
    mox.StubOutWithMock(simulador, 'analiza_resultado_e_acumula_gols')

    partida = FakeModel('partida')
    partida.realizada = True
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 2
    
    simulador.analiza_resultado_e_acumula_gols.__call__(3, 2, 1, partida, False).AndReturn(partida.time_1)
    mox.ReplayAll()
    try:
        vitorioso = simulador.obter_time_na_partida(partida, False)    
        assert_equals(vitorioso, partida.time_1)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obter_vitorioso_na_partida_nao_realizada():
    mox = Mox()
    mox.StubOutWithMock(simulador, 'analiza_resultado_e_acumula_gols')

    partida = FakeModel('partida')
    partida.realizada = False
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.palpites_time_1 = 1
    partida.palpites_time_2 = 2
    partida.votos = 1

    simulador.analiza_resultado_e_acumula_gols.__call__(1, 2, 1, partida, False).AndReturn(partida.time_2)
    mox.ReplayAll()
    try:
        vitorioso = simulador.obter_time_na_partida(partida, False)
        assert_equals(vitorioso, partida.time_2)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_analiza_resultado_retorna_none_quando_empate():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 3

    time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)

    assert_equals(time, None)

def test_analiza_resultado_retorna_time_1_perdedor():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 1
    partida.gols_time_2 = 2

    time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, True)

    assert_equals(time, partida.time_1)

def test_analiza_resultado_retorna_time_1():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 3
    partida.gols_time_2 = 2

    time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)

    assert_equals(time, partida.time_1)

def test_analiza_resultado_retorna_time_2():
    partida = FakeModel('partida')
    partida.time_1 = FakeModel('time1')
    partida.time_2 = FakeModel('time2')
    partida.gols_time_1 = 2
    partida.gols_time_2 = 3

    time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)

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
    mox.StubOutWithMock(simulador, 'adiciona_item_a_lista')
    mox.StubOutWithMock(simulador, 'ordenar_por_saldo_de_gols_removendo_empatados_da_original')
    mox.StubOutWithMock(simulador, 'reposiciona_e_reordena_na_original')

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
        
    simulador.adiciona_item_a_lista.__call__([], 1)
    simulador.adiciona_item_a_lista.__call__([], 2)
    simulador.adiciona_item_a_lista.__call__([], time2)
    simulador.adiciona_item_a_lista.__call__([], time3)
    
    simulador.ordenar_por_saldo_de_gols_removendo_empatados_da_original.__call__([], times)
    simulador.reposiciona_e_reordena_na_original.__call__([], [], times)

    mox.ReplayAll()
    try:
        simulador.normalizar_lista_com_saldo_de_gols(times)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
