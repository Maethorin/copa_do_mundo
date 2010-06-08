#!/usr/bin/env python
# encoding: utf-8

import parser_regra
from copa_do_mundo.tabela.models import *
from django.db.models import Q

def obtem_times_de_partida_de_oitavas(regra):
    grupos = parser_regra.obtem_grupos_de_regra(regra)
    classificacoes = parser_regra.obtem_classificacoes_de_regra(regra)
    time1 = obtem_time_do_grupo_na_classificacao(grupos[0], classificacoes[0])
    time2 = obtem_time_do_grupo_na_classificacao(grupos[1], classificacoes[1])
    return time1, time2

def obtem_time_do_grupo_na_classificacao(nome_do_grupo, classificacao):
    times = Time.objects.filter(grupo__nome__exact=nome_do_grupo)
    for time in times:
        partidas = Partida.objects.filter(Q(time_1__id__exact=time.id) | Q(time_2__id__exact=time.id))
        for partida in partidas:
            vitorioso = obter_vitorioso_na_partida(partida)
            if vitorioso == None:
                time.pontos += 1
            elif vitorioso.id == time.id:
                time.pontos += 2

    times.sort(lambda x, y: cmp(y.pontos, x.pontos))

    normalizar_lista_com_saldo_de_gols(times)
    
    return times[classificacao - 1]

def obter_vitorioso_na_partida(partida):
    if partida.realizada:
        return analiza_resultado(partida.gols_time_1, partida.gols_time_2, partida)

    return analiza_resultado(partida.palpites_time_1, partida.palpites_time_2, partida)

def analiza_resultado(valor_1, valor_2, partida):
    if valor_1 == valor_2:
        return None
    if valor_1 > valor_2:
        return partida.time_1
    return partida.time_2

def normalizar_lista_com_saldo_de_gols(times):
    reordena = False
    times_com_pontos_iguais = []
    for i in range(0, (len(times) - 1)):
        if times[i].pontos == times[i + 1].pontos:
            adiciona_time_a_lista(times_com_pontos_iguais, times[i])
            adiciona_time_a_lista(times_com_pontos_iguais, times[i + 1])
            reordena = True

    if reordena:
        for time in times_com_pontos_iguais:
            times.remove(time)
        obter_saldos_de_gols(times_com_pontos_iguais)
        times_com_pontos_iguais.sort(lambda x, y: cmp(y.saldo_de_gols, x.saldo_de_gols))
        times.extend(times_com_pontos_iguais)

def adiciona_time_a_lista(lista, time):
    if not time in lista:
        lista.append(time)

def obter_saldos_de_gols(times):
    for time in times:
        time.saldo_de_gols = time.gols_feitos - time.gols_tomados