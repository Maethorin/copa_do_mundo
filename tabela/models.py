#!/usr/bin/env python
# encoding: utf-8

import datetime
from django.conf import settings
from django.db import models


class Grupo(models.Model):
    id = models.AutoField(primary_key=True, db_column='grupo_id')
    nome = models.CharField(max_length=1, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Grupos'
        db_table = 'grupos'

    def __unicode__(self):
        return "Grupo {}".format(self.nome)


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
        if self.jogos == 0:
            return 0
        return round(float(self.vitorias) / float(self.jogos) * 100, 1)

    class Meta:
        ordering = ['grupo', '-pontos', 'nome']
        verbose_name_plural = 'Times'
        db_table = 'times'

    def __unicode__(self):
        return '%s - Grupo %s. Pontos %d' % (self.nome, self.grupo.nome, self.pontos)


class Fase(models.Model):
    class Meta:
        verbose_name_plural = 'Fases'
        db_table = 'fases'

    id = models.AutoField(primary_key=True, db_column='fase_id')
    nome = models.CharField(max_length=20)
    slug = models.SlugField(null=True)

    def __unicode__(self):
        return u"%s" % self.nome


class Estadio(models.Model):
    class Meta:
        ordering = ('nome',)
        verbose_name_plural = 'Estadios'
        db_table = 'estadios'

    id = models.AutoField(primary_key=True, db_column='estadio_id')
    nome = models.CharField(max_length=20)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=200, default='')

    def cidade_e_estado(self):
        return u"%s-%s" % (self.cidade, self.estado)

    def __unicode__(self):
        return u"%s (%s-%s)" % (self.nome, self.cidade, self.estado)


class Partida(models.Model):
    id = models.AutoField(primary_key=True, db_column='partida_id')
    time_1 = models.ForeignKey(Time, related_name='time_1', null=True, blank=True)
    time_2 = models.ForeignKey(Time, related_name='time_2', null=True, blank=True)
    data = models.DateTimeField()
    local = models.ForeignKey(Estadio, null=True)
    fase = models.ForeignKey(Fase, null=True)
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
        formato_data = '%a %d %B - %H:%M'
        situacao = "Realizada" if self.realizada else u"Não realizada"
        if self.time_1:
            return u'%s - %s x %s - %s - %s - %s' % (
                self.fase,
                self.time_1.nome,
                self.time_2.nome,
                self.data.strftime(formato_data),
                situacao,
                self.local
            )
        return u'%s - %s - %s - %s - %s' % (
            self.fase,
            self.regra_para_times,
            self.data.strftime(formato_data),
            situacao,
            self.local
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

        if not vitorioso or not palpite:
            return "EMPATE"

        if vitorioso == palpite:
            return "CERTO"

        if vitorioso and palpite:
            if vitorioso.nome == palpite.nome:
                return "CERTO"
        return "ERRADO"

    def palpite_certo(self):
        return self.media_palpites_time_1() == int(self.gols_time_1 or 0) and self.media_palpites_time_2() == int(self.gols_time_2)

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

    def registra_palpite(self, palpite_time_1, palpite_time_2):
        if not self.votos:
            self.votos = 0
            self.palpites_time_1 = 0
            self.palpites_time_2 = 0
        self.votos += 1
        self.palpites_time_1 += palpite_time_1
        self.palpites_time_2 += palpite_time_2
        self.save()
