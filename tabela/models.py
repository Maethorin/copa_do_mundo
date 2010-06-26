#!/usr/bin/env python
# encoding: utf-8

import locale
import datetime
from django.db import models
from copa_do_mundo import settings

class Grupo(models.Model):
    id = models.AutoField(primary_key=True, db_column='grupo_id')
    nome = models.CharField(max_length=1, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Grupos'
        db_table = 'grupos'

    def __unicode__(self):
        return self.nome

class Time(models.Model):
    id = models.AutoField(primary_key=True, db_column='time_id')
    nome = models.CharField(max_length=200, unique=True)
    pontos = models.IntegerField(blank=True, default=0)
    grupo = models.ForeignKey(Grupo)
    abreviatura = models.CharField(max_length=15, unique=True, blank=True, null=True)
    sigla = models.CharField(max_length=3, unique=True, blank=True, null=True)
    
    jogos = 0
    vitorias = 0
    empates = 0
    gols_feitos = 0
    gols_tomados = 0
    saldo_de_gols = 0

    def derrotas(self):
        return self.jogos - (self.vitorias + self.empates)

    def aproveitamento(self):
        return round(float(self.vitorias) / float(self.jogos) * 100, 1)

    class Meta:
        ordering = ['grupo', '-pontos', 'nome']
        verbose_name_plural = 'Times'
        db_table = 'times'

    def __unicode__(self):
        return '%s - Grupo %s. Pontos %d' % (self.nome, self.grupo.nome, self.pontos)

class Partida(models.Model):
    id = models.AutoField(primary_key=True, db_column='partida_id')
    time_1 = models.ForeignKey(Time, related_name='time_1', null=True, blank=True)
    time_2 = models.ForeignKey(Time, related_name='time_2', null=True, blank=True)
    data = models.DateTimeField()
    rodada = models.CharField(max_length=200)
    regra_para_times = models.CharField(max_length=20, null=True, blank=True)
    gols_time_1 = models.IntegerField(null=True, blank=True)
    gols_time_2 = models.IntegerField(null=True, blank=True)
    palpites_time_1 = models.IntegerField(null=True, blank=True)
    palpites_time_2 = models.IntegerField(null=True, blank=True)
    realizada = models.BooleanField()
    votos = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['data']
        verbose_name_plural = 'Partidas'
        db_table = 'partidas'

    def __unicode__(self):
        #locale.setlocale(locale.LC_ALL, 'pt_BR')
        formato_data = '%a %d %B - %H:%M'
        if self.time_1:
            return '%s - %s x %s - %s' % (
                self.rodada, 
                self.time_1.nome, 
                self.time_2.nome, 
                self.data.strftime(formato_data)
            )
        return '%s - %s - %s' % (
            self.rodada, 
            self.regra_para_times, 
            self.data.strftime(formato_data)
        )

    def vitorioso_certo(self):
        vitorioso = None
        if self.gols_time_1 > self.gols_time_2:
            vitorioso = self.time_1
        elif self.gols_time_2 > self.gols_time_1:
            vitorioso = self.time_2
        
        palpite = None
        if self.media_palpites_time_1() > self.media_palpites_time_2():
            palpite = self.time_1
        elif self.media_palpites_time_2() > self.media_palpites_time_1():
            palpite = self.time_2

        if vitorioso == palpite:
            return True
        if vitorioso and palpite:
            if vitorioso.nome == palpite.nome:
                return True
        return False

    def palpite_certo(self):
        return self.media_palpites_time_1() == int(self.gols_time_1) and self.media_palpites_time_2() == int(self.gols_time_2)

    def em_andamento(self):
        data_atual = datetime.datetime.today()
        data_atual = data_atual + datetime.timedelta(hours=settings.SERVER_TIME_DIFF)
        data_limite = self.data + datetime.timedelta(minutes=-3)
        if data_limite <= data_atual and not self.realizada:
            return True
        return False

    def time_eh_diferente(self, time1, time2):
        if self.time_1 is None:
            return True
        if self.time_2 is None:
            return True
        if time1 and self.time_1.id != time1.id:
            return True
        if time2 and self.time_2.id != time2.id:
            return True
        return False

    def media_palpites_time_1(self):
        if not self.votos or self.votos < 0:
            return 0
        return self.palpites_time_1 / self.votos

    def media_palpites_time_2(self):
        if not self.votos or self.votos < 0:
            return 0
        return self.palpites_time_2 / self.votos