# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Total.addition_coefficients'
        db.add_column(u'game_total', 'addition_coefficients',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Total.addition_coefficients'
        db.delete_column(u'game_total', 'addition_coefficients')


    models = {
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'black_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black_player'", 'to': u"orm['player.Player']"}),
            'btime_limit': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 8, 14, 0, 0)', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Round']"}),
            'start': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 8, 13, 0, 0)', 'blank': 'True'}),
            'steps': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '8196', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'white_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'white_player'", 'to': u"orm['player.Player']"}),
            'wtime_limit': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 8, 14, 0, 0)', 'blank': 'True'})
        },
        u'game.round': {
            'Meta': {'object_name': 'Round'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'couples': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'draws': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'draw'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'loser'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            'report': ('django.db.models.fields.CharField', [], {'max_length': '8192'}),
            'start': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 13, 0, 0)', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'total': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Total']"}),
            'winners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'winner'", 'blank': 'True', 'to': u"orm['player.Player']"})
        },
        u'game.total': {
            'Meta': {'object_name': 'Total'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'addition_coefficients': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['player.Player']", 'symmetrical': 'False', 'blank': 'True'}),
            'time_rule': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'player.player': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('playername', 'birth_date'),)", 'object_name': 'Player'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'coefficientK': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'color_list': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '4'}),
            'country': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degree': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_self_player': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'place': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'playername': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {'default': '50', 'db_index': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'sex': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['game']