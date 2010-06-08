# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Grupo'
        db.create_table('grupos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='grupo_id')),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1)),
        ))
        db.send_create_signal('tabela', ['Grupo'])

        # Adding model 'Time'
        db.create_table('times', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='time_id')),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('pontos', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tabela.Grupo'])),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('tabela', ['Time'])

        # Adding model 'Partida'
        db.create_table('partidas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='partida_id')),
            ('time_1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='time_1', null=True, to=orm['tabela.Time'])),
            ('time_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='time_2', null=True, to=orm['tabela.Time'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')()),
            ('rodada', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('regra_para_times', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('gols_time_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gols_time_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('palpites_time_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('palpites_time_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('realizada', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('votos', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('tabela', ['Partida'])


    def backwards(self, orm):
        
        # Deleting model 'Grupo'
        db.delete_table('grupos')

        # Deleting model 'Time'
        db.delete_table('times')

        # Deleting model 'Partida'
        db.delete_table('partidas')


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
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tabela.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'time_id'"}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['tabela']
