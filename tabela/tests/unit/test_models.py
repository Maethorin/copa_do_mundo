#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

from nose.tools import assert_equals
from tabela import models


def test_valida_unicode_de_grupo():
    grupo = models.Grupo()
    grupo.nome = 'A'
    grupo_str = '%s' % grupo
    assert_equals(grupo_str, 'Grupo A')


def test_valida_unicode_de_time():
    time = models.Time()
    time.nome = 'Time 1'
    time.grupo = models.Grupo()
    time.grupo.nome = 'A'
    time.pontos = 10
    time_str = '%s' % time
    assert_equals(time_str, 'Time 1 - Grupo A. Pontos 10')


def test_valida_unicode_de_partida_com_times():
    partida = models.Partida()
    partida.fase = models.Fase(nome="Oitavas")
    partida.local = models.Estadio(nome="Estadio", cidade="Cidade", estado="RJ")
    partida.time_1 = models.Time()
    partida.time_1.nome = 'Time 1'
    partida.time_2 = models.Time()
    partida.time_2.nome = 'Time 2'
    partida.data = datetime(2014, 6, 12, 8, 30)
    partida_str = u'%s' % partida
    assert_equals(partida_str, u'Oitavas - Time 1 x Time 2 - Thu 12 June - 08:30 - Não realizada - Estadio (Cidade-RJ)')


def test_valida_unicode_de_partida_com_regra():
    partida = models.Partida()
    partida.fase = models.Fase(nome="Oitavas")
    partida.local = models.Estadio(nome="Estadio", cidade="Cidade", estado="RJ")
    partida.regra_para_times = '1Ax2B'
    partida.data = datetime(2010, 6, 5, 8, 30)
    partida.realizada = True
    partida_str = '%s' % partida
    assert_equals(partida_str, 'Oitavas - 1Ax2B - Sat 05 June - 08:30 - Realizada - Estadio (Cidade-RJ)')


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
