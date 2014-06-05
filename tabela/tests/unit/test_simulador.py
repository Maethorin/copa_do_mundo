#!/usr/bin/env python
# encoding: utf-8
import os

import mox
from nose.tools import assert_equals

from lxml import html as lhtml

from django.template import Context, Template

from tabela import simulador, models


class TestSimulador(mox.MoxTestBase):

    def test_obter_time_de_partidas_com_partidas_de_oitavas(self):
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
        self.mox.StubOutWithMock(simulador, 'atualiza_informacoes_de_partida_em_andamento')

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)
        regra = 'O43x44'

        partida1 = self.mox.CreateMock(models.Partida)
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = "Oitavas"
        partida1.vitorioso = time1
        partida1.regra_para_times = regra
        partida1.realizada = False

        partida2 = self.mox.CreateMock(models.Partida)
        partida2.vitorioso = None
        partida2.fase = self.mox.CreateMock(models.Fase)
        partida2.fase.nome = "Oitavas"
        partida2.regra_para_times = regra
        partida2.realizada = False

        partidas = [partida1, partida2]

        simulador.obtem_times_de_partida_de_oitavas(regra).AndReturn([time1, time2])
        simulador.obtem_times_de_partida_de_oitavas(regra).AndReturn([time2, time1])
        partida1.time_eh_diferente(time1, time2).AndReturn(False)
        partida2.time_eh_diferente(time2, time1).AndReturn(False)

        simulador.atualiza_informacoes_de_partida_em_andamento(partida1)
        simulador.atualiza_informacoes_de_partida_em_andamento(partida2)

        partida1.save()
        partida2.save()

        self.mox.ReplayAll()
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)

    def test_obter_time_de_partidas_com_partidas_de_outras_fases(self):
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_outras_fases')
        self.mox.StubOutWithMock(simulador, 'atualiza_informacoes_de_partida_em_andamento')

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)
        regra = 'Q43x44'

        partida1 = self.mox.CreateMock(models.Partida)
        partida1.vitorioso = time1
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = "Quartas"
        partida1.regra_para_times = regra
        partida1.realizada = False

        partida2 = self.mox.CreateMock(models.Partida)
        partida2.vitorioso = None
        partida2.fase = self.mox.CreateMock(models.Fase)
        partida2.fase.nome = "Quartas"
        partida2.regra_para_times = regra
        partida2.realizada = False

        partidas = [partida1, partida2]

        simulador.obtem_times_de_partida_de_outras_fases(regra).AndReturn([time1, time2])
        simulador.obtem_times_de_partida_de_outras_fases(regra).AndReturn([time2, time1])

        partida1.time_eh_diferente(time1, time2).AndReturn(False)
        partida2.time_eh_diferente(time2, time1).AndReturn(False)

        simulador.atualiza_informacoes_de_partida_em_andamento(partida1)
        simulador.atualiza_informacoes_de_partida_em_andamento(partida2)

        partida1.save()
        partida2.save()
        self.mox.ReplayAll()
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)

    def test_obter_time_de_partidas_com_partidas_de_outras_fases_e_de_oitavas(self):
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_outras_fases')
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
        self.mox.StubOutWithMock(simulador, 'atualiza_informacoes_de_partida_em_andamento')

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)
        regra = 'Q43x44'

        partida1 = self.mox.CreateMock(models.Partida)
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = "Quartas"
        partida1.vitorioso = time1
        partida1.regra_para_times = regra
        partida1.realizada = False

        partida2 = self.mox.CreateMock(models.Partida)
        partida2.vitorioso = None
        partida2.fase = self.mox.CreateMock(models.Fase)
        partida2.fase.nome = "Oitavas"
        partida2.regra_para_times = regra
        partida2.realizada = False

        partidas = [partida1, partida2]

        simulador.obtem_times_de_partida_de_outras_fases(regra).AndReturn([time1, time2])
        simulador.obtem_times_de_partida_de_oitavas(regra).AndReturn([time2, time1])

        partida1.time_eh_diferente(time1, time2).AndReturn(False)
        partida2.time_eh_diferente(time2, time1).AndReturn(False)

        simulador.atualiza_informacoes_de_partida_em_andamento(partida1)
        simulador.atualiza_informacoes_de_partida_em_andamento(partida2)

        partida1.save()
        partida2.save()
        self.mox.ReplayAll()
        simulador.obter_times_de_partidas(partidas)
        assert_equals(time1, partida1.time_1)
        assert_equals(time2, partida1.time_2)
        assert_equals(time2, partida2.time_1)
        assert_equals(time1, partida2.time_2)

    def test_obtem_times_de_partida_de_oitavas(self):
        self.mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
        self.mox.StubOutWithMock(simulador, 'parser_regra')

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)
        regra = '1Ax2B'
        grupos = ['A', 'B']
        classificacoes = ['1', '2']

        simulador.parser_regra.obtem_grupos_de_regra(regra).AndReturn(grupos)
        simulador.parser_regra.obtem_classificacoes_de_regra(regra).AndReturn(classificacoes)

        simulador.obtem_time_do_grupo_na_classificacao(grupos[0], classificacoes[0]).AndReturn(time1)
        simulador.obtem_time_do_grupo_na_classificacao(grupos[1], classificacoes[1]).AndReturn(time2)

        self.mox.ReplayAll()
        time_a, time_b = simulador.obtem_times_de_partida_de_oitavas(regra)
        assert_equals(time1, time_a)
        assert_equals(time2, time_b)

    def test_obtem_times_de_partida_de_outras_fases_com_regra_de_oitavas(self):
        self.mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
        self.mox.StubOutWithMock(simulador, 'parser_regra')
        self.mox.StubOutWithMock(simulador, 'Partida')
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
        self.mox.StubOutWithMock(simulador, 'obter_time_na_partida')

        regra = 'O53x54'
        simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
        simulador.parser_regra.eh_disputa_de_terceiro_lugar(regra).AndReturn(False)
        simulador.Partida.objects = self.mox.CreateMockAnything()
        partida1 = self.mox.CreateMock(models.Partida)
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = "Oitavas"
        partida1.regra_para_times = 'O56x57'

        partida2 = self.mox.CreateMock(models.Partida)
        partida2.regra_para_times = 'O51x52'

        simulador.Partida.objects.get(id='53').AndReturn(partida1)
        simulador.Partida.objects.get(id='54').AndReturn(partida2)

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)
        simulador.obtem_times_de_partida_de_oitavas('O56x57').AndReturn((time1, time2))
        simulador.obtem_times_de_partida_de_oitavas('O51x52').AndReturn((time2, time1))

        simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

        self.mox.ReplayAll()
        time_a, time_b = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, time_a)
        assert_equals(time2, time_b)

    def test_obtem_times_de_partida_de_outras_fases_com_regra_de_outras_fases(self):
        self.mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
        self.mox.StubOutWithMock(simulador, 'parser_regra')
        self.mox.StubOutWithMock(simulador, 'Partida')
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
        self.mox.StubOutWithMock(simulador, 'obter_time_na_partida')

        regra = 'O53x54'
        simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
        simulador.parser_regra.eh_disputa_de_terceiro_lugar(regra).AndReturn(False)
        simulador.Partida.objects = self.mox.CreateMockAnything()
        partida1 = self.mox.CreateMock(models.Partida)
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = "Quartas"
        partida1.regra_para_times = 'Q56x57'
        partida2 = self.mox.CreateMock(models.Partida)
        partida2.regra_para_times = 'Q51x52'

        partida3 = self.mox.CreateMock(models.Partida)
        partida3.fase = self.mox.CreateMock(models.Fase)
        partida3.fase.nome = "Oitavas"
        partida3.regra_para_times = 'O53x54'
        partida4 = self.mox.CreateMock(models.Partida)
        partida4.regra_para_times = 'O58x59'

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)

        simulador.Partida.objects.get(id='53').AndReturn(partida1)
        simulador.Partida.objects.get(id='54').AndReturn(partida2)

        simulador.parser_regra.obtem_ids_de_partida_de_regra(partida1.regra_para_times).AndReturn(['56', '57'])
        simulador.parser_regra.eh_disputa_de_terceiro_lugar(partida1.regra_para_times).AndReturn(False)
        simulador.Partida.objects.get(id='56').AndReturn(partida3)
        simulador.Partida.objects.get(id='57').AndReturn(partida4)

        simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
        simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

        simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

        simulador.parser_regra.obtem_ids_de_partida_de_regra(partida2.regra_para_times).AndReturn(['51', '52'])
        simulador.parser_regra.eh_disputa_de_terceiro_lugar(partida2.regra_para_times).AndReturn(False)
        simulador.Partida.objects.get(id='51').AndReturn(partida3)
        simulador.Partida.objects.get(id='52').AndReturn(partida4)

        simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
        simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

        simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

        simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

        self.mox.ReplayAll()
        time_a, time_b = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, time_a)
        assert_equals(time2, time_b)

    def test_obtem_times_de_partida_de_disputa_de_terceiro_lugar(self):
        self.mox.StubOutWithMock(simulador, 'obtem_time_do_grupo_na_classificacao')
        self.mox.StubOutWithMock(simulador, 'parser_regra')
        self.mox.StubOutWithMock(simulador, 'Partida')
        self.mox.StubOutWithMock(simulador, 'obtem_times_de_partida_de_oitavas')
        self.mox.StubOutWithMock(simulador, 'obter_time_na_partida')

        regra = 'O53x54'
        simulador.Partida.objects = self.mox.CreateMockAnything()
        partida1 = self.mox.CreateMock(models.Partida)
        partida1.fase = self.mox.CreateMock(models.Fase)
        partida1.fase.nome = 'Quartas'
        partida1.regra_para_times = 'Q56x57'
        partida2 = self.mox.CreateMock(models.Partida)
        partida2.regra_para_times = 'Q51x52'

        partida3 = self.mox.CreateMock(models.Partida)
        partida3.fase = self.mox.CreateMock(models.Fase)
        partida3.fase.nome = 'Oitavas'
        partida3.regra_para_times = 'O53x54'
        partida4 = self.mox.CreateMock(models.Partida)
        partida4.regra_para_times = 'O58x59'

        time1 = self.mox.CreateMock(models.Time)
        time2 = self.mox.CreateMock(models.Time)

        simulador.parser_regra.obtem_ids_de_partida_de_regra(regra).AndReturn(['53', '54'])
        simulador.Partida.objects.get(id='53').AndReturn(partida1)
        simulador.Partida.objects.get(id='54').AndReturn(partida2)
        simulador.parser_regra.eh_disputa_de_terceiro_lugar('O53x54').AndReturn(False)

        simulador.parser_regra.obtem_ids_de_partida_de_regra(partida1.regra_para_times).AndReturn(['56', '57'])
        simulador.Partida.objects.get(id='56').AndReturn(partida3)
        simulador.Partida.objects.get(id='57').AndReturn(partida4)
        simulador.parser_regra.eh_disputa_de_terceiro_lugar('Q56x57').AndReturn(False)

        simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
        simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

        simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

        simulador.parser_regra.obtem_ids_de_partida_de_regra(partida2.regra_para_times).AndReturn(['51', '52'])
        simulador.Partida.objects.get(id='51').AndReturn(partida3)
        simulador.Partida.objects.get(id='52').AndReturn(partida4)

        simulador.parser_regra.eh_disputa_de_terceiro_lugar('Q51x52').AndReturn(False)
        simulador.obtem_times_de_partida_de_oitavas('O53x54').AndReturn((time1, time2))
        simulador.obtem_times_de_partida_de_oitavas('O58x59').AndReturn((time2, time1))

        simulador.obter_time_na_partida(partida3, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida4, False).AndReturn((time2, 2, 3))

        simulador.obter_time_na_partida(partida1, False).AndReturn((time1, 2, 3))
        simulador.obter_time_na_partida(partida2, False).AndReturn((time2, 2, 3))

        self.mox.ReplayAll()
        time_a, time_b = simulador.obtem_times_de_partida_de_outras_fases(regra)
        assert_equals(time1, time_a)
        assert_equals(time2, time_b)

    def test_obtem_time_do_grupo_na_classificacao(self):
        self.mox.StubOutWithMock(simulador, 'obtem_times_do_grupo_ordenados_por_classificacao')
        simulador.obtem_times_do_grupo_ordenados_por_classificacao('A').AndReturn(['timeA', 'timeB'])
        simulador.obtem_times_do_grupo_ordenados_por_classificacao('B').AndReturn(['timeC', 'timeB'])
        self.mox.ReplayAll()
        retorno = simulador.obtem_time_do_grupo_na_classificacao('A', 1)
        assert_equals(retorno, 'timeA')
        retorno = simulador.obtem_time_do_grupo_na_classificacao('B', 2)
        assert_equals(retorno, 'timeB')

    def test_obtem_times_do_grupo_ordenados_por_classificacao(self):
        self.mox.StubOutWithMock(simulador, 'normalizar_lista_com_saldo_de_gols')
        self.mox.StubOutWithMock(simulador, 'soma_gols_do_time')
        self.mox.StubOutWithMock(simulador, 'obter_time_na_partida')
        self.mox.StubOutWithMock(simulador, 'Time')
        self.mox.StubOutWithMock(simulador, 'Partida')
        self.mox.StubOutWithMock(simulador, 'Fase')
        self.mox.StubOutWithMock(simulador, 'Q')

        time1 = self.mox.CreateMock(models.Time)
        time1.id = 1
        time1.pontos = 2
        time2 = self.mox.CreateMock(models.Time)
        time2.id = 2
        time2.pontos = 0
        times = [time1, time2]

        simulador.Time.objects = self.mox.CreateMockAnything()
        simulador.Time.objects.filter(grupo__nome__exact='A').AndReturn(times)
        simulador.Partida.objects = self.mox.CreateMockAnything()
        simulador.Fase.objects = self.mox.CreateMockAnything()

        partida1 = self.mox.CreateMock(models.Partida)
        partida1.vitorioso = time1
        partida1.time_1 = time1
        partida1.time_2 = time2

        partida2 = self.mox.CreateMock(models.Partida)
        partida2.vitorioso = None
        partida2.time_1 = time1
        partida2.time_2 = time2

        partidas = [partida1, partida2]

        for time in times:
            simulador.Fase.objects.get(slug='classificacao').AndReturn("Fase")
            simulador.Q(fase='Fase').AndReturn(True)
            simulador.Q(time_1__id__exact=time.id).AndReturn(True)
            simulador.Q(time_2__id__exact=time.id).AndReturn(True)
            simulador.Partida.objects.filter(True | True).AndReturn(partidas)
            for partida in partidas:
                simulador.obter_time_na_partida(partida).AndReturn((partida.vitorioso, 0, 0))
                simulador.soma_gols_do_time(time, 0, 0, partida.time_1.id)

        simulador.normalizar_lista_com_saldo_de_gols(times)
        self.mox.ReplayAll()
        retorno = simulador.obtem_times_do_grupo_ordenados_por_classificacao('A')
        assert_equals(retorno, [time1, time2])

    def test_obter_vitorioso_na_partida_realizada(self):
        self.mox.StubOutWithMock(simulador, 'analiza_resultado_e_acumula_gols')

        partida = self.mox.CreateMock(models.Time)
        partida.realizada = True
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.gols_time_1 = 3
        partida.gols_time_2 = 2

        simulador.analiza_resultado_e_acumula_gols(3, 2, 1, partida, False).AndReturn(partida.time_1)
        self.mox.ReplayAll()
        vitorioso = simulador.obter_time_na_partida(partida, False)
        assert_equals(vitorioso, partida.time_1)

    def test_obter_vitorioso_na_partida_nao_realizada(self):
        self.mox.StubOutWithMock(simulador, 'analiza_resultado_e_acumula_gols')

        partida = self.mox.CreateMock(models.Partida)
        partida.realizada = False
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.palpites_time_1 = 1
        partida.palpites_time_2 = 2
        partida.votos = 1

        simulador.analiza_resultado_e_acumula_gols(1, 2, 1, partida, False).AndReturn(partida.time_2)
        self.mox.ReplayAll()
        vitorioso = simulador.obter_time_na_partida(partida, False)
        assert_equals(vitorioso, partida.time_2)

    def test_analiza_resultado_retorna_none_quando_empate(self):
        partida = self.mox.CreateMock(models.Partida)
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.gols_time_1 = 3
        partida.gols_time_2 = 3
        time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)
        assert_equals(time, None)

    def test_analiza_resultado_retorna_time_1_perdedor(self):
        partida = self.mox.CreateMock(models.Partida)
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.gols_time_1 = 1
        partida.gols_time_2 = 2

        time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, True)

        assert_equals(time, partida.time_1)

    def test_analiza_resultado_retorna_time_1(self):
        partida = self.mox.CreateMock(models.Partida)
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.gols_time_1 = 3
        partida.gols_time_2 = 2

        time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)

        assert_equals(time, partida.time_1)

    def test_analiza_resultado_retorna_time_2(self):
        partida = self.mox.CreateMock(models.Partida)
        partida.time_1 = self.mox.CreateMock(models.Time)
        partida.time_2 = self.mox.CreateMock(models.Time)
        partida.gols_time_1 = 2
        partida.gols_time_2 = 3

        time, gol1, gol2 = simulador.analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, False)

        assert_equals(time, partida.time_2)

    def test_normalizar_lista_com_saldo_de_gols_quando_nao_ha_empate_nada_faz(self):
        time1 = self.mox.CreateMock(models.Time)
        time1.id = 1
        time1.pontos = 4
        time2 = self.mox.CreateMock(models.Time)
        time2.id = 2
        time2.pontos = 2
        time3 = self.mox.CreateMock(models.Time)
        time3.id = 3
        time3.pontos = 1
        times = [time1, time2, time3]

        simulador.normalizar_lista_com_saldo_de_gols(times)

        assert_equals(times[0], time1)
        assert_equals(times[1], time2)
        assert_equals(times[2], time3)

    def test_normalizar_lista_com_saldo_de_gols_recupera_saldo_quando_ha_empate(self):
        self.mox.StubOutWithMock(simulador, 'adiciona_item_a_lista')
        self.mox.StubOutWithMock(simulador, 'ordenar_por_saldo_de_gols_removendo_empatados_da_original')
        self.mox.StubOutWithMock(simulador, 'reposiciona_e_reordena_na_original')

        time1 = self.mox.CreateMock(models.Time)
        time1.id = 1
        time1.pontos = 4
        time2 = self.mox.CreateMock(models.Time)
        time2.id = 2
        time2.pontos = 2
        time3 = self.mox.CreateMock(models.Time)
        time3.id = 3
        time3.pontos = 2
        times = [time1, time2, time3]

        simulador.adiciona_item_a_lista([], 1)
        simulador.adiciona_item_a_lista([], 2)
        simulador.adiciona_item_a_lista([], time2)
        simulador.adiciona_item_a_lista([], time3)

        simulador.ordenar_por_saldo_de_gols_removendo_empatados_da_original([], times)
        simulador.reposiciona_e_reordena_na_original([], [], times)

        self.mox.ReplayAll()
        try:
            simulador.normalizar_lista_com_saldo_de_gols(times)
            self.mox.VerifyAll()
        finally:
            self.mox.UnsetStubs()


class TestPegaPlacaDaGlobo(mox.MoxTestBase):

    def obter_html_de_placar(self, partidas):
        template_file = open(os.path.join(os.path.abspath("unit/placar-globo.html")), "r")
        template_string = template_file.read()
        template = Template(template_string)
        template_file.close()
        c = Context({"partidas": partidas})
        return template.render(c)

    def cria_partida(self, time_1_nome, time_1_abreviatura, time_1_gols, time_2_nome, time_2_abreviatura, time_2_gols):
        partida = models.Partida()
        partida.time_1 = models.Time()
        partida.time_1.nome = time_1_nome
        partida.time_1.abreviatura = time_1_abreviatura
        partida.gols_time_1 = time_1_gols

        partida.time_2 = models.Time()
        partida.time_2.nome = time_2_nome
        partida.time_2.abreviatura = time_2_abreviatura
        partida.gols_time_2 = time_2_gols
        return partida

    def test_le_corretamente_com_placar_primeira_partida(self):
        partida1 = self.cria_partida("P1 Blah1", "P1B1", 2, "P1 Blah2", "P1B2", 1)
        partida2 = self.cria_partida("P2 Blah1", "P2B1", 3, "P2 Blah2", "P2B2", 0)
        html = self.obter_html_de_placar([partida1, partida2])
        pagina_resultado = lhtml.fragment_fromstring(html, create_parent=True)
        placar = simulador.obtem_placar_do_html(pagina_resultado, partida1)
        assert_equals(placar.gols_time_1, '2')
        assert_equals(placar.gols_time_2, '1')

    def test_le_corretamente_com_placar_segunda_partida(self):
        partida1 = self.cria_partida("P1 Blah1", "P1B1", 2, "P1 Blah2", "P1B2", 1)
        partida2 = self.cria_partida("P2 Blah1", "P2B1", 3, "P2 Blah2", "P2B2", 0)
        html = self.obter_html_de_placar([partida1, partida2])
        pagina_resultado = lhtml.fragment_fromstring(html, create_parent=True)
        placar = simulador.obtem_placar_do_html(pagina_resultado, partida2)
        assert_equals(placar.gols_time_1, '3')
        assert_equals(placar.gols_time_2, '0')
