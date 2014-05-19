# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Time.gols_feitos'
        db.delete_column('times', 'gols_feitos')

        # Deleting field 'Time.gols_tomados'
        db.delete_column('times', 'gols_tomados')

        # Adding field 'Time.sigla'
        db.add_column('times', 'sigla',
                      self.gf('django.db.models.fields.CharField')(max_length=3, unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Time.gols_feitos'
        db.add_column('times', 'gols_feitos',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'Time.gols_tomados'
        db.add_column('times', 'gols_tomados',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Deleting field 'Time.sigla'
        db.delete_column('times', 'sigla')


    models = {
        'tabela.grupo': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Grupo', 'db_table': "'grupos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'grupo_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'})
        },
        'tabela.partida': {
            'Meta': {'ordering': "['data']", 'object_name': 'Partida', 'db_table': "'partidas'"},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'gols_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gols_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'partida_id'"}),
            'palpites_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'palpites_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'realizada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'regra_para_times': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rodada': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_1'", 'null': 'True', 'to': "orm['tabela.Time']"}),
            'time_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_2'", 'null': 'True', 'to': "orm['tabela.Time']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'tabela.time': {
            'Meta': {'ordering': "['grupo', '-pontos', 'nome']", 'object_name': 'Time', 'db_table': "'times'"},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tabela.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'time_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tabela']