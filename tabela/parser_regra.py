#!/usr/bin/env python
# encoding: utf-8

import re

def regra_eh_da_primeira_fase(regra):
    return re.match(r"[1-2]", regra) != None

def obtem_grupos_de_regra(regra):
    if not regra_eh_da_primeira_fase(regra):
        raise ValueError(u'A regra precisa ser da primeira fase para se obter grupos. Ex.: 1Ax2B')
    return re.findall(r"[A-H]", regra)

def obtem_classificacoes_de_regra(regra):
    if not regra_eh_da_primeira_fase(regra):
        raise ValueError(u'A regra precisa ser da primeira fase para se obter classificações. Ex.: 1Ax2B')
    return re.findall(r"[1-2]", regra)

def obtem_ids_de_partida_de_regra(regra):
    if not re.match(r"[A-Z][0-9]{2}x[0-9]{2}", regra):
        raise ValueError(u'A regra não combina com regras de partidas que não seja da primeira fase: %s' % regra)
    return re.findall(r"[0-9]{2}", regra)

def eh_disputa_de_terceiro_lugar(regra):
    return re.match(r"P", regra) != None