#!/usr/bin/env python
# encoding: utf-8

from mox import *
from nose.tools import assert_equals

from copa_do_mundo.tabela import parser_regra

def test_parser_regra_retorna_true_se_regra_da_partida_eh_da_primeira_fase():
    assert_equals(parser_regra.regra_eh_da_primeira_fase('1Ax2B'), True)

def test_parser_regra_retorna_false_se_regra_da_partida_nao_eh_da_primeira_fase():
    assert_equals(parser_regra.regra_eh_da_primeira_fase('O53x52'), False)

def test_parser_regra_retorna_false_se_regra_da_partida_nao_eh_da_primeira_fase_com_numero_maior_que_dois():
    assert_equals(parser_regra.regra_eh_da_primeira_fase('3Ax4B'), False)

def test_parser_regra_retorna_false_se_regra_da_partida_nao_eh_da_primeira_fase_com_1_no_meio_da_regra():
    assert_equals(parser_regra.regra_eh_da_primeira_fase('O51x52'), False)

def test_obtem_grupos_de_regra():
    assert_equals(parser_regra.obtem_grupos_de_regra('1Ax2B'), ['A', 'B'])

def test_obtem_classificacoes_de_regra():
    assert_equals(parser_regra.obtem_classificacoes_de_regra('1Ax2B'), ['1', '2'])

def test_obtem_grupos_de_regra_dispara_erro_se_regra_nao_eh_da_primeira_fase():
    try:
        parser_regra.obtem_grupos_de_regra('O52x53')
        assert False
    except ValueError:
        assert True

def test_obtem_classificacoes_de_regra_dispara_erro_se_regra_nao_eh_da_primeira_fase():
    try:
        parser_regra.obtem_classificacoes_de_regra('O52x53')
        assert False
    except ValueError:
        assert True