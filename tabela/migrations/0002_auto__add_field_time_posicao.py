# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Time.posicao'
        db.add_column('times', 'posicao',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Time.posicao'
        db.delete_column('times', 'posicao')


    models = {
        u'tabela.estadio': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'Estadio', 'db_table': "'estadios'"},
            'cidade': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'estadio_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'tabela.fase': {
            'Meta': {'object_name': 'Fase', 'db_table': "'fases'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'fase_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        u'tabela.grupo': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Grupo', 'db_table': "'grupos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'grupo_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'})
        },
        u'tabela.partida': {
            'Meta': {'ordering': "['data']", 'object_name': 'Partida', 'db_table': "'partidas'"},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'fase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tabela.Fase']", 'null': 'True'}),
            'gols_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gols_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'partida_id'"}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tabela.Estadio']", 'null': 'True'}),
            'palpites_time_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'palpites_time_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'realizada': ('django.db.models.fields.BooleanField', [], {}),
            'regra_para_times': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'time_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_1'", 'null': 'True', 'to': u"orm['tabela.Time']"}),
            'time_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'time_2'", 'null': 'True', 'to': u"orm['tabela.Time']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'tabela.time': {
            'Meta': {'ordering': "['grupo', '-pontos', 'nome']", 'object_name': 'Time', 'db_table': "'times'"},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tabela.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'time_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'posicao': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tabela']