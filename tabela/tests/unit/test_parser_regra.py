#!/usr/bin/env python
# encoding: utf-8

from mox import *
from nose.tools import assert_equals

from tabela import parser_regra


def test_parser_regra_retorna_true_se_regra_da_partida_eh_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    regra = '1Ax2B'
    parser_regra.re.match(r"[1-2]", regra).AndReturn('Alguma coisa')

    mox.ReplayAll()
    try:
        retorno = parser_regra.regra_eh_da_primeira_fase(regra)
        assert_equals(retorno, True)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_grupos_de_regra_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    mox.StubOutWithMock(parser_regra, 'regra_eh_da_primeira_fase')
    regra = '1Ax2B'
    parser_regra.regra_eh_da_primeira_fase.__call__(regra).AndReturn(True)
    parser_regra.re.findall(r"[A-H]", regra).AndReturn(['A', 'B'])

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_grupos_de_regra(regra)
        assert_equals(retorno, ['A', 'B'])
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_classificacoes_de_regra_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    mox.StubOutWithMock(parser_regra, 'regra_eh_da_primeira_fase')
    regra = '1Ax2B'
    parser_regra.regra_eh_da_primeira_fase.__call__(regra).AndReturn(True)
    parser_regra.re.findall(r"[1-2]", regra).AndReturn([1, 2])

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_classificacoes_de_regra(regra)
        assert_equals(retorno, [1, 2])
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_obtem_grupos_dispara_erro_se_regra_nao_eh_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 'regra_eh_da_primeira_fase')

    regra = 'O51x52'
    parser_regra.regra_eh_da_primeira_fase.__call__(regra).AndReturn(False)

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_grupos_de_regra(regra)
        assert False
    except ValueError, e:
        mox.VerifyAll()
        assert_equals(e.message, u'A regra precisa ser da primeira fase para se obter grupos. Ex.: 1Ax2B')
    finally:
        mox.UnsetStubs()        

def test_obtem_classificacoes_dispara_erro_se_regra_nao_eh_regra_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 'regra_eh_da_primeira_fase')

    regra = 'O51x52'
    parser_regra.regra_eh_da_primeira_fase.__call__(regra).AndReturn(False)

    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_classificacoes_de_regra(regra)
        assert False
    except ValueError, e:
        mox.VerifyAll()
        assert_equals(e.message, u'A regra precisa ser da primeira fase para se obter classificações. Ex.: 1Ax2B')
    finally:
        mox.UnsetStubs()

def test_obtem_ids_de_partida_de_regra():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    parser_regra.re.match(r"[A-Z][0-9]{2}x[0-9]{2}", 'O53x54').AndReturn('AlgumaCoisa')
    parser_regra.re.findall(r"[0-9]{2}", 'O53x54').AndReturn(['53', '54'])
    
    mox.ReplayAll()
    try:
        retorno = parser_regra.obtem_ids_de_partida_de_regra('O53x54')
        mox.VerifyAll()
        assert_equals(['53', '54'], retorno)
    finally:
        mox.UnsetStubs()
    
def test_obtem_ids_de_partida_de_regra_dispara_erro_se_passar_regra_da_primeira_fase():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    parser_regra.re.match(r"[A-Z][0-9]{2}x[0-9]{2}", '1Ax2B').AndReturn(None)
    mox.ReplayAll()
    try:
        parser_regra.obtem_ids_de_partida_de_regra('1Ax2B')
        assert False
    except ValueError, e:
        mox.VerifyAll()
        assert_equals(e.message, u'A regra não combina com regras de partidas que não seja da primeira fase: 1Ax2B')
    finally:
        mox.UnsetStubs()

def test_eh_disputa_de_terceiro_lugar_retorna_true():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    parser_regra.re.match(r"P", 'P53x54').AndReturn('AlgumaCoisa')
    mox.ReplayAll()
    try:
        retorno = parser_regra.eh_disputa_de_terceiro_lugar('P53x54')
        mox.VerifyAll()
        assert retorno
    finally:
        mox.UnsetStubs()

def test_eh_disputa_de_terceiro_lugar_retorna_false():
    mox = Mox()
    mox.StubOutWithMock(parser_regra, 're')
    parser_regra.re.match(r"P", 'V53x54').AndReturn(None)
    mox.ReplayAll()
    try:
        retorno = parser_regra.eh_disputa_de_terceiro_lugar('V53x54')
        mox.VerifyAll()
        assert not retorno
    finally:
        mox.UnsetStubs()
    