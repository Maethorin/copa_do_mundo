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
