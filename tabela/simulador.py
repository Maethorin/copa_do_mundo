#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings

import parser_regra

from django.db.models import Q
from lxml import html as lhtml
from tabela.models import Partida, Time, Fase


class InformacoesDePartida():
    def __init__(self, placar, status="Tá Indo"):
        self.gols_time_1 = 0
        self.gols_time_2 = 0
        if len(placar) == 2:
            self.gols_time_1 = placar[0]
            self.gols_time_2 = placar[1]
        self.realizada = status == 'Finished'


def obtem_partidas_de_grupo(grupo):
    fase = Fase.objects.get(nome='Classificação')
    times_query = Q(fase=fase, time_1__in=grupo.time_set.all()) | Q(fase=fase, time_2__in=grupo.time_set.all())
    partidas = Partida.objects.filter(times_query)
    return partidas


def obter_dados_de_times(grupos, atual=False):
    for grupo in grupos:
        grupo.times = obtem_times_do_grupo_ordenados_por_classificacao(grupo.nome, atual)


def obter_times_de_partidas(partidas):
    for partida in partidas:
        if partida.fase.nome == 'Oitavas':
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
            atualiza_informacoes_de_partida_em_andamento(partida)
            partida.save()


def atualiza_informacoes_de_partida_em_andamento(partida):
    if partida.em_andamento():
        informacoes = obter_informacoes_da_partida_em_jogo(partida)
        if informacoes:
            partida.gols_time_1 = informacoes.gols_time_1
            partida.gols_time_2 = informacoes.gols_time_2
            partida.realizada = informacoes.realizada


def obter_rodada(partida):
    if 12 <= partida.data.day <= 16:
        return "1"
    elif partida.data.day == 17 and partida.time_1.grupo.nome == "H":
        return "1"
    elif partida.data.day == 17 and partida.time_1.grupo.nome == "A":
        return "2"
    elif 18 <= partida.data.day <= 22:
            return "2"
    return "3"


def obter_informacoes_da_partida_em_jogo(partida):
    try:
        url = settings.URL_BASE_DE_RESULTADOS
        if partida.fase.slug == "classificacao":
            url_grupo = settings.URL_RESULTADOS_DE_CLASSIFICACAO.format(settings.URL_DE_GRUPOS[partida.time_1.grupo.nome], obter_rodada(partida))
            url = "{}{}".format(url, url_grupo)
        pagina_resultado = lhtml.parse(url).getroot()
    except IOError:
        return None
    if pagina_resultado is None:
        return None

    equipes = pagina_resultado.cssselect(".nome-equipe")
    placar = []
    for equipe in equipes:
        if equipe.text == partida.time_1.abreviatura:
            placar.append(equipe.getparent().getparent().cssselect(".placar-mandante").text)
        elif equipe.text == partida.time_2.abreviatura:
            placar.append(equipe.getparent().getparent().cssselect(".placar-visitante").text)

    if placar:
        return InformacoesDePartida(placar)
    return None


def obtem_times_de_partida_de_outras_fases(regra):
    ids = parser_regra.obtem_ids_de_partida_de_regra(regra)
    partida1 = Partida.objects.get(id=ids[0])
    partida2 = Partida.objects.get(id=ids[1])
    perdedor = False
    if partida1.fase.nome == 'Oitavas':
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


def obtem_times_do_grupo_ordenados_por_classificacao(nome_do_grupo, atual=False):
    times = Time.objects.filter(grupo__nome__exact=nome_do_grupo)
    times_lista = []
    for time in times:
        fase = Fase.objects.get(slug='classificacao')
        filtros = Q(fase=fase) & (Q(time_1__id__exact=time.id) | Q(time_2__id__exact=time.id))
        if atual:
            filtros = filtros & Q(realizada=True)
        partidas = Partida.objects.filter(filtros)
        for partida in partidas:
            vitorioso, gols_time_1, gols_time_2 = obter_time_na_partida(partida)
            soma_gols_do_time(time, gols_time_1, gols_time_2, partida.time_1.id)
            time.jogos += 1
            if vitorioso is None:
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


def obter_partidas_em_andamento():
    em_andamento = []
    partidas = Partida.objects.all()
    for partida in partidas:
        if partida.em_andamento():
            em_andamento.append(partida)
    return em_andamento


def reordena_partidas_para_chave(fase):
    lista_acima = []
    lista_abaixo = []
    regras_juntas = [['1Ax2B', '1Cx2D', '1Ex2F', '1Gx2H'], ['1Dx2C', '1Bx2A', '1Fx2E', '1Hx2G']]
    if fase.slug == 'oitavas':
        for partida in fase.partida_set.all():
            if partida.regra_para_times in regras_juntas[0]:
                lista_acima.append(partida)
            if partida.regra_para_times in regras_juntas[1]:
                lista_abaixo.append(partida)
        lista_acima.extend(lista_abaixo)
        fase.partidas = lista_acima