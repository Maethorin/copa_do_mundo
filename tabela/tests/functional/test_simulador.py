#!/usr/bin/env python
# encoding: utf-8

from nose.tools import assert_equals
from copa_do_mundo.tabela import simulador

class FakeModel():
    def __init__(self, nome):
        self.nome = nome
    
    def __repr__(self):
        return self.nome

def test_normalizar_lista_com_saldo_de_gols_recupera_saldo_quando_ha_empate():
    time1 = FakeModel('time1')
    time1.id = 1
    time1.pontos = 4
    time2 = FakeModel('time2')
    time2.id = 2
    time2.pontos = 2
    time2.gols_feitos = 1
    time2.gols_tomados = 0
    time3 = FakeModel('time3')
    time3.id = 3
    time3.pontos = 2
    time3.gols_feitos = 2
    time3.gols_tomados = 0
    times = [time1, time2, time3]

    simulador.normalizar_lista_com_saldo_de_gols(times)

    assert_equals(times[1], time3)

def test_obtem_times_de_partida_de_oitavas():
    time1, time2 = simulador.obtem_times_de_partida_de_oitavas('1Ax2B')
    
    assert_equals(time1.nome, )