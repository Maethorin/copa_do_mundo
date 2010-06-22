#!/usr/bin/env python
# encoding: utf-8

from nose.tools import assert_equals
from copa_do_mundo.tabela import simulador
from copa_do_mundo.tabela.models import *

class FakeModel():

    def __init__(self, nome):
        self.nome = nome
    
    def __repr__(self):
        return self.nome

def test_normalizar_lista_com_saldo_de_gols_recupera_saldo_quando_ha_empate():
    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 4
    time1.gols_feitos = 3
    time1.gols_tomados = 0
    time1.saldo_de_gols = time1.gols_feitos - time1.gols_tomados
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 4
    time2.gols_feitos = 1
    time2.gols_tomados = 0
    time2.saldo_de_gols = time2.gols_feitos - time2.gols_tomados
    time3 = FakeModel('time3')
    time3.id = 3
    time3.pontos = 2
    time3.gols_feitos = 2
    time3.gols_tomados = 0
    time3.saldo_de_gols = time3.gols_feitos - time3.gols_tomados
    time4 = FakeModel('time4')
    time4.id = 4
    time4.pontos = 2
    time4.gols_feitos = 3
    time4.gols_tomados = 0
    time4.saldo_de_gols = time4.gols_feitos - time4.gols_tomados

    time5 = FakeModel('time5')
    time5.id = 5
    time5.pontos = 5
    time6 = FakeModel('time6')
    time6.id = 6
    time6.pontos = 6
    time7 = FakeModel('time7')
    time7.id = 7
    time7.pontos = 1
    time7.gols_feitos = 0
    time7.gols_tomados = 0
    time7.saldo_de_gols = time7.gols_feitos - time7.gols_tomados
    time8 = FakeModel('time8')
    time8.id = 8
    time8.pontos = 1
    time8.gols_feitos = 3
    time8.gols_tomados = 0
    time8.saldo_de_gols = time8.gols_feitos - time8.gols_tomados
    time9 = FakeModel('time9')
    time9.id = 9
    time9.pontos = 1
    time9.gols_feitos = 3
    time9.gols_tomados = 2
    time9.saldo_de_gols = time9.gols_feitos - time9.gols_tomados

    times = [time1, time2, time3, time4, time5, time6, time7, time8, time9]

    simulador.normalizar_lista_com_saldo_de_gols(times)

    assert_equals(times, [time1, time2, time4, time3, time5, time6, time8, time9, time7])

def test_obtem_times_de_partida_de_oitavas():
    time1, time2 = simulador.obtem_times_de_partida_de_oitavas('1Ax2B')
    
    assert_equals(time1.nome, 'Uruguai')
    assert_equals(time2.nome, 'Coréia do Sul')
