#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.db.models import Q


class Grupo(models.Model):
    id = models.AutoField(primary_key=True, db_column='grupo_id')
    nome = models.CharField(max_length=1, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Grupos'
        db_table = 'grupos'

    def __unicode__(self):
        return "Grupo {}".format(self.nome)

    def times_por_classificacao_simulada(self):
        return self.time_set.all().order_by('-classificacao_simulada__pontos', '-classificacao_simulada__saldo_de_gols', '-classificacao_simulada__gols_feitos')

    def times_por_classificacao_real(self):
        return self.time_set.all().order_by('-classificacao_real__pontos', '-classificacao_real__saldo_de_gols', '-classificacao_real__gols_feitos')

    def partidas_do_grupo_na_fase(self, fase_slug):
        fase = Fase.objects.get(slug=fase_slug)
        times_query = Q(fase=fase, time_1__in=self.time_set.all()) | Q(fase=fase, time_2__in=self.time_set.all())
        if fase.tem_rodadas:
            return Partida.objects.filter(times_query).order_by('rodada__id')
        return Partida.objects.filter(times_query)


class Classificacao(models.Model):
    TIPO_CLASSIFICACAO = (("S", "Simulada"), ("R", "Real"))
    tipo = models.CharField(max_length=1, choices=TIPO_CLASSIFICACAO, default="S")
    jogos = models.IntegerField(blank=True, default=0)
    vitorias = models.IntegerField(blank=True, default=0)
    empates = models.IntegerField(blank=True, default=0)
    gols_feitos = models.IntegerField(blank=True, default=0)
    gols_tomados = models.IntegerField(blank=True, default=0)
    saldo_de_gols = models.IntegerField(blank=True, default=0)
    pontos = models.IntegerField(blank=True, default=0)
    posicao = models.IntegerField(blank=True, default=0)

    def aproveitamento(self):
        if self.jogos == 0:
            return 0
        return round(float(self.vitorias) / float(self.jogos) * 100, 1)

    def derrotas(self):
        return self.jogos - (self.vitorias + self.empates)

    def zera_valores(self):
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.gols_feitos = 0
        self.gols_tomados = 0
        self.pontos = 0

    class Meta:
        verbose_name = u'Classificação'
        verbose_name_plural = u'Classificações'
        db_table = 'classificacao'


class Time(models.Model):
    id = models.AutoField(primary_key=True, db_column='time_id')
    nome = models.CharField(max_length=200, unique=True)
    grupo = models.ForeignKey(Grupo)
    abreviatura = models.CharField(max_length=15, unique=True, blank=True, null=True)
    sigla = models.CharField(max_length=3, unique=True, blank=True, null=True)
    classificacao_simulada = models.OneToOneField(Classificacao, null=True, related_name="time_na_simulacao")
    classificacao_real = models.OneToOneField(Classificacao, null=True, related_name="time_real")

    def classificacao(self, tipo):
        if tipo == "S":
            return self.classificacao_simulada
        elif tipo == "R":
            return self.classificacao_real

    def zera_valores(self, tipo):
        if tipo == "S":
            if self.classificacao_simulada:
                try:
                    self.classificacao_simulada.zera_valores()
                except Classificacao.DoesNotExist:
                    self.classificacao_simulada = Classificacao.objects.create(tipo="S")
                    self.save()
            else:
                self.classificacao_simulada = Classificacao.objects.create(tipo="S")
                self.save()
        elif tipo == "R":
            if self.classificacao_real:
                try:
                    self.classificacao_real.zera_valores()
                except Classificacao.DoesNotExist:
                    self.classificacao_real = Classificacao.objects.create(tipo="R")
                    self.save()
            else:
                self.classificacao_real = Classificacao.objects.create(tipo="R")
                self.save()

    def derrotas(self):
        return self.jogos - (self.vitorias + self.empates)

    def aproveitamento(self):
        if self.jogos == 0:
            return 0
        return round(float(self.vitorias) / float(self.jogos) * 100, 1)

    def classificado(self):
        fase = Fase.fase_atual()
        if not fase:
            return True
        if fase.slug == 'classificacao' and fase.finalizada:
            return self.classificacao_real.posicao <= 2
        if fase.slug == 'classificacao' and not fase.finalizada:
            return True
        if fase.slug != 'classificacao':
            for partida in fase.partida_set.all():
                if self == partida.time_1 or self == partida.time_2:
                    return True
        return False

    class Meta:
        ordering = ['grupo', 'nome']
        verbose_name_plural = 'Times'
        db_table = 'times'

    def __unicode__(self):
        return '%s - Grupo %s.' % (self.nome, self.grupo.nome)


class Rodada(models.Model):
    id = models.AutoField(primary_key=True, db_column='rodada_id')
    nome = models.CharField(max_length=20)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name_plural = 'Rodadas'
        db_table = 'rodadas'

    def __unicode__(self):
        return u"{}".format(self.nome)


class Fase(models.Model):
    class Meta:
        verbose_name_plural = 'Fases'
        db_table = 'fases'

    id = models.AutoField(primary_key=True, db_column='fase_id')
    nome = models.CharField(max_length=20)
    slug = models.SlugField(null=True)
    data_inicio = models.DateTimeField(null=True)
    data_fim = models.DateTimeField(null=True)
    tem_rodadas = models.BooleanField(default=False)

    @property
    def eh_atual(self):
        hoje = datetime.now()
        return self.data_inicio <= hoje <= self.data_fim

    @property
    def finalizada(self):
        hoje = datetime.now()
        return hoje > self.data_fim

    @classmethod
    def fase_atual(cls):
        for fase in cls.objects.all():
            if fase.eh_atual:
                return fase
        return None

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
    rodada = models.ForeignKey(Rodada, null=True)
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

    def formatado_para_placar(self):
        time_1 = u"Não definido"
        time_2 = u"Não definido"
        if self.time_1:
            time_1 = self.time_1.nome
        if self.time_2:
            time_2 = self.time_2.nome
        return u"{} x {}".format(time_1, time_2)

    def obter_nome_de_time(self, time):
        if time:
            return time.nome
        return u"Não definido"

    def __unicode__(self):
        formato_data = '%a %d %B - %H:%M'
        situacao = "Realizada" if self.realizada else u"Não realizada"
        if self.time_1 or self.time_2:
            return u'%s - %s x %s - %s - %s - %s' % (
                self.fase,
                self.obter_nome_de_time(self.time_1),
                self.obter_nome_de_time(self.time_2),
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

        if not vitorioso and not palpite:
            return "EMPATE"

        if not vitorioso and palpite:
            return "ERRADO"

        if vitorioso == palpite:
            return "CERTO"

        if vitorioso and palpite:
            if vitorioso.nome == palpite.nome:
                return "CERTO"
        return "ERRADO"

    def palpite_certo(self):
        return self.media_palpites_time_1() == int(self.gols_time_1 or 0) and self.media_palpites_time_2() == int(self.gols_time_2 or 0)

    def em_andamento(self):
        data_atual = datetime.today()
        data_atual = data_atual + timedelta(hours=settings.SERVER_TIME_DIFF)
        data_limite = self.data + timedelta(minutes=-3)
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
