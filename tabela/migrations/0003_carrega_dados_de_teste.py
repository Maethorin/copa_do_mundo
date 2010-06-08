# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from copa_do_mundo.tabela.model import *

class Migration(DataMigration):

    def forwards(self, orm):
        grupoA = Grupo(nome='A')
        grupoA.save()
        grupoB = Grupo(nome='B')
        grupoB.save()
        time1 = Time(nome='Time 1', grupo=grupoA, gols_feitos=3, gols_tomados=0, pontos=3)
        time2 = Time(nome='Time 2', grupo=grupoA, gols_feitos=1, gols_tomados=0, pontos=2)
        time3 = Time(nome='Time 3', grupo=grupoB, gols_feitos=4, gols_tomados=2, pontos=2)
        time4 = Time(nome='Time 4', grupo=grupoB, gols_feitos=2, gols_tomados=2, pontos=2)
        time1.save()
        time2.save()
        time3.save()
        time4.save()
        partida1 = Partida(nome='')

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'tabela.grupo': {
            'Meta': {'object_name': 'Grupo', 'db_table': "'grupos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'grupo_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'})
        },
        'tabela.partida': {
            'Meta': {'object_name': 'Partida', 'db_table': "'partidas'"},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'gols_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gols_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'partida_id'"}),
            'palpites_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'palpites_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'realizada': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'regra_para_times': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rodada': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_1'", 'null': 'True', 'to': "orm['tabela.Time']"}),
            'time_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_2'", 'null': 'True', 'to': "orm['tabela.Time']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'tabela.time': {
            'Meta': {'object_name': 'Time', 'db_table': "'times'"},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'gols_feitos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'gols_tomados': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tabela.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'time_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['tabela']
