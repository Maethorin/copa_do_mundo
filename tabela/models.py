#!/usr/bin/env python
# encoding: utf-8

import locale
from django.db import models

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
    gols_feitos = models.IntegerField(blank=True, default=0)
    gols_tomados = models.IntegerField(blank=True, default=0)
    grupo = models.ForeignKey(Grupo)
    abreviatura = models.CharField(max_length=15, unique=True, blank=True, null=True)

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
        locale.setlocale(locale.LC_ALL, 'pt_BR')
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
    
    def media_palpites_time_1(self):
        if not self.votos or self.votos < 0:
            return 0
        return self.palpites_time_1 / self.votos

    def media_palpites_time_2(self):
        if not self.votos or self.votos < 0:
            return 0
        return self.palpites_time_2 / self.votos