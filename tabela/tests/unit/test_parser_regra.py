#!/usr/bin/env python
# encoding: utf-8

from mox import *
from nose.tools import assert_equals

from copa_do_mundo.tabela import parser_regra

def test_parser_regra_retorna_true_se_regra_da_partida_eh_da_primeira_fase():
    mox = Mox()
    parser_regra.re = mox.CreateMockAnything()
    regra = '1Ax2B'
    parser_regra.re.match(r"[1-2]", regra).AndReturn('Alguma coisa')

    mox.ReplayAll()
    retorno = parser_regra.regra_eh_da_primeira_fase(regra)
    mox.VerifyAll()
    
    assert_equals(retorno, True)

def test_obtem_grupos_de_regra_da_primeira_fase():
    mox = Mox()
    parser_regra.re = mox.CreateMockAnything()
    regra = '1Ax2B'
    parser_regra.regra_eh_da_primeira_fase = lambda regra : True
    parser_regra.re.findall(r"[A-H]", regra).AndReturn(['A', 'B'])

    mox.ReplayAll()
    retorno = parser_regra.obtem_grupos_de_regra(regra)
    mox.VerifyAll()

    assert_equals(retorno, ['A', 'B'])

def test_obtem_classificacoes_de_regra_da_primeira_fase():
    mox = Mox()
    parser_regra.re = mox.CreateMockAnything()
    regra = '1Ax2B'
    parser_regra.regra_eh_da_primeira_fase = lambda regra : True
    parser_regra.re.findall(r"[1-2]", regra).AndReturn([1, 2])

    mox.ReplayAll()
    retorno = parser_regra.obtem_classificacoes_de_regra(regra)
    mox.VerifyAll()
    
    assert_equals(retorno, [1, 2])

def test_obtem_grupos_dispara_erro_se_regra_nao_eh_da_primeira_fase():
    mox = Mox()
    parser_regra.re = mox.CreateMockAnything()
    regra = 'O51x52'
    parser_regra.regra_eh_da_primeira_fase = lambda regra : False

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_grupos_de_regra(regra)
        assert False
    except ValueError, e:
        assert_equals(e.message, u'A regra precisa ser da primeira fase para se obter grupos. Ex.: 1Ax2B')
        
    mox.VerifyAll()

def test_obtem_classificacoes_dispara_erro_se_regra_nao_eh_regra_da_primeira_fase():
    mox = Mox()
    parser_regra.re = mox.CreateMockAnything()
    regra = 'O51x52'
    parser_regra.regra_eh_da_primeira_fase = lambda regra : False

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_classificacoes_de_regra(regra)
        assert False
    except ValueError, e:
        assert_equals(e.message, u'A regra precisa ser da primeira fase para se obter classificações. Ex.: 1Ax2B')

    mox.VerifyAll()
