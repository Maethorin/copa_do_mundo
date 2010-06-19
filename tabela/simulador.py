#!/usr/bin/env python
# encoding: utf-8

import parser_regra
from copa_do_mundo.tabela.models import *
from django.db.models import Q

def obter_dados_de_times(grupos):
    for grupo in grupos:
        grupo.times = obtem_times_do_grupo_ordenados_por_classificacao(grupo.nome)

def obter_times_de_partidas(partidas):
    for partida in partidas:
        time1 = None
        time2 = None
        if partida.rodada == 'oitavas':
            time1, time2 = obtem_times_de_partida_de_oitavas(partida.regra_para_times)
        else:
            time1, time2 = obtem_times_de_partida_de_outras_fases(partida.regra_para_times)
        
        if not partida.realizada:
            if partida.time_eh_diferente(time1, time2):
                partida.palpites_time_1 = 0
                partida.palpites_time_2 = 0
                partida.votos = 0

            partida.time_1 = time1
            partida.time_2 = time2
            partida.save()

def obtem_times_de_partida_de_outras_fases(regra):
    ids = parser_regra.obtem_ids_de_partida_de_regra(regra)
    partida1 = Partida.objects.get(id=ids[0])
    partida2 = Partida.objects.get(id=ids[1])
    perdedor = False
    if partida1.rodada == 'oitavas':
        partida1.time_1, partida1.time_2 = obtem_times_de_partida_de_oitavas(partida1.regra_para_times)
        partida2.time_1, partida2.time_2 = obtem_times_de_partida_de_oitavas(partida2.regra_para_times)
    elif parser_regra.eh_disputa_de_terceiro_lugar(regra):
        partida1.time_1, partida1.time_2 = obtem_times_de_partida_de_outras_fases(partida1.regra_para_times)
        partida2.time_1, partida2.time_2 = obtem_times_de_partida_de_outras_fases(partida2.regra_para_times)
        perdedor = True
    else:
        partida1.time_1, partida1.time_2 = obtem_times_de_partida_de_outras_fases(partida1.regra_para_times)
        partida2.time_1, partida2.time_2 = obtem_times_de_partida_de_outras_fases(partida2.regra_para_times)
    time1, gols_time_1, gols_time_2 = obter_time_na_partida(partida1, perdedor)
    time2, gols_time_1, gols_time_2 = obter_time_na_partida(partida2, perdedor)
    
    return time1, time2

def obtem_times_de_partida_de_oitavas(regra):
    grupos = parser_regra.obtem_grupos_de_regra(regra)
    classificacoes = parser_regra.obtem_classificacoes_de_regra(regra)
    time1 = obtem_time_do_grupo_na_classificacao(grupos[0], classificacoes[0])
    time2 = obtem_time_do_grupo_na_classificacao(grupos[1], classificacoes[1])
    return time1, time2
    
def obtem_time_do_grupo_na_classificacao(nome_do_grupo, classificacao):
    classificacao = int(classificacao)
    times = obtem_times_do_grupo_ordenados_por_classificacao(nome_do_grupo) 
    return times[classificacao - 1]

def obtem_times_do_grupo_ordenados_por_classificacao(nome_do_grupo):
    times = Time.objects.filter(grupo__nome__exact=nome_do_grupo)
    times_lista = []
    for time in times:
        partidas = Partida.objects.filter(Q(rodada__startswith='rodada_') & (Q(time_1__id__exact=time.id) | Q(time_2__id__exact=time.id)))
        for partida in partidas:
            vitorioso, gols_time_1, gols_time_2 = obter_time_na_partida(partida)
            soma_gols_do_time(time, gols_time_1, gols_time_2, partida.time_1.id)
            time.jogos += 1
            if vitorioso == None:
                time.pontos += 1
                time.empates += 1
            elif vitorioso.id == time.id:
                time.pontos += 3
                time.vitorias += 1
            time.saldo_de_gols = time.gols_feitos - time.gols_tomados
        times_lista.append(time)

    times_lista.sort(lambda x, y: cmp(y.pontos, x.pontos))

    normalizar_lista_com_saldo_de_gols(times_lista)
    return times_lista

def obter_time_na_partida(partida, perdedor=False):
    if partida.realizada:
        return analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, perdedor)

    return analiza_resultado_e_acumula_gols(partida.palpites_time_1, partida.palpites_time_2, partida.votos, partida, perdedor)

def analiza_resultado_e_acumula_gols(valor_1, valor_2, votos, partida, perdedor):
    if not valor_1:
        valor_1 = 0
    if not valor_2:
        valor_2 = 0
    gols_time_1 = valor_1
    gols_time_2 = valor_2
    if votos > 0:
        gols_time_1 = valor_1 / votos
        gols_time_2 = valor_2 / votos

    if gols_time_1 == gols_time_2:
        return None, gols_time_1, gols_time_2
    if gols_time_1 > gols_time_2:
        if perdedor:
            return partida.time_2, gols_time_1, gols_time_2
        return partida.time_1, gols_time_1, gols_time_2

    if perdedor:
        return partida.time_1, gols_time_1, gols_time_2        
    return partida.time_2, gols_time_1, gols_time_2

def soma_gols_do_time(time, gols_time_1, gols_time_2, time_1_id):
    if time.id == time_1_id:
        time.gols_feitos += gols_time_1
        time.gols_tomados += gols_time_2
    else:
        time.gols_feitos += gols_time_2
        time.gols_tomados += gols_time_1

def normalizar_lista_com_saldo_de_gols(times):
    for i in range(0, len(times)):
        times[i].posicao = i + 1

    reordena = False
    lista_de_empates = []
    indices_dos_empatados = []
    indices_com_pontos_iguais = []
    times_com_pontos_iguais = []
    indices_dos_empatados = []
    for i in range(0, len(times)):
        if (i + 1) < len(times) and times[i].pontos == times[i + 1].pontos:
            adiciona_item_a_lista(indices_com_pontos_iguais, i)
            adiciona_item_a_lista(indices_com_pontos_iguais, i + 1)
            adiciona_item_a_lista(times_com_pontos_iguais, times[i])
            adiciona_item_a_lista(times_com_pontos_iguais, times[i + 1])
            reordena = True
        else:
            if len(times_com_pontos_iguais) > 0:
                lista_de_empates.append(times_com_pontos_iguais)
                indices_dos_empatados.append(indices_com_pontos_iguais)
                times_com_pontos_iguais = []
                indices_com_pontos_iguais = []

    if reordena:
        ordenar_por_saldo_de_gols_removendo_empatados_da_original(lista_de_empates, times)
        reposiciona_e_reordena_na_original(lista_de_empates, indices_dos_empatados, times)

def ordenar_por_saldo_de_gols_removendo_empatados_da_original(lista_de_empates, times):
    for times_empatados in lista_de_empates:
        for time in times_empatados:
            times.remove(time)
        times_empatados.sort(lambda x, y: cmp(y.saldo_de_gols, x.saldo_de_gols))

def reposiciona_e_reordena_na_original(lista_de_empates, indices_dos_empatados, times):  
    for i in range(0, len(lista_de_empates)):
        for k in range(0, len(lista_de_empates[i])):
            lista_de_empates[i][k].posicao = indices_dos_empatados[i][k] + 1

        times.extend(lista_de_empates[i])

    times.sort(lambda x, y: cmp(x.posicao, y.posicao))

def adiciona_item_a_lista(lista, item):
    if not item in lista:
        lista.append(item)
