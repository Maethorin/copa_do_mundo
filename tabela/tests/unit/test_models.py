#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

from mox import *
from nose.tools import assert_equals
from copa_do_mundo.tabela import models

def test_valida_unicode_de_grupo():
    grupo = models.Grupo()
    grupo.nome = 'A'
    grupo_str = '%s' % grupo
    assert_equals(grupo_str, 'A')

def test_valida_unicode_de_time():
    time = models.Time()
    time.nome = 'Time 1'
    time.grupo = models.Grupo()
    time.grupo.nome = 'A'
    time.pontos = 10
    time_str = '%s' % time
    assert_equals(time_str, 'Time 1 - Grupo A. Pontos 10')

def test_valida_unicode_de_partida_com_times():
    mox = Mox()
    models.locale = mox.CreateMockAnything()
    models.locale.LC_ALL = 'Alguma Coisa'
    models.locale.setlocale('Alguma Coisa', 'pt_BR')
    partida = models.Partida()
    partida.rodada = '1 Rodada'
    partida.time_1 = models.Time()
    partida.time_1.nome = 'Time 1'
    partida.time_2 = models.Time()
    partida.time_2.nome = 'Time 2'
    partida.data = datetime(2010, 6, 5, 8, 30)
    partida_str = '%s' % partida
    assert_equals(partida_str, '1 Rodada - Time 1 x Time 2 - Sat 05 June - 08:30')

def test_valida_unicode_de_partida_com_regra():
    mox = Mox()
    models.locale = mox.CreateMockAnything()
    models.locale.LC_ALL = 'Alguma Coisa'
    models.locale.setlocale('Alguma Coisa', 'pt_BR')
    partida = models.Partida()
    partida.rodada = '1 Rodada'
    partida.regra_para_times = '1Ax2B'
    partida.data = datetime(2010, 6, 5, 8, 30)
    partida_str = '%s' % partida
    assert_equals(partida_str, '1 Rodada - 1Ax2B - Sat 05 June - 08:30')

def test_media_time_1_palpites_em_partida_retorna_zero_se_votos_eh_igual_a_zero():
    partida = models.Partida()
    partida.votos = 0
    
    media = partida.media_palpites_time_1()
    
    assert_equals(media, 0)

def test_media_time_2_palpites_em_partida_retorna_zero_se_votos_eh_igual_a_zero():
    partida = models.Partida()
    partida.votos = 0

    media = partida.media_palpites_time_2()

    assert_equals(media, 0)

def test_media_time_1_palpites_em_partida_retorna_correto():
    partida = models.Partida()
    partida.votos = 2
    partida.palpites_time_1 = 4

    media = partida.media_palpites_time_1()

    assert_equals(media, 2)

def test_media_time_2_palpites_em_partida_retorna_correto():
    partida = models.Partida()
    partida.votos = 2
    partida.palpites_time_2 = 4

    media = partida.media_palpites_time_2()

    assert_equals(media, 2)
    