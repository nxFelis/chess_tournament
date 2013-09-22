# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Elo', fields ['contestant']
        db.delete_unique(u'player_elo', ['contestant_id'])

        # Removing unique constraint on 'Elo', fields ['player']
        db.delete_unique(u'player_elo', ['player_id'])


        # Changing field 'Elo.player'
        db.alter_column(u'player_elo', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player']))

        # Changing field 'Elo.contestant'
        db.alter_column(u'player_elo', 'contestant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player']))

    def backwards(self, orm):

        # Changing field 'Elo.player'
        db.alter_column(u'player_elo', 'player_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['player.Player'], unique=True))
        # Adding unique constraint on 'Elo', fields ['player']
        db.create_unique(u'player_elo', ['player_id'])


        # Changing field 'Elo.contestant'
        db.alter_column(u'player_elo', 'contestant_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['player.Player']))
        # Adding unique constraint on 'Elo', fields ['contestant']
        db.create_unique(u'player_elo', ['contestant_id'])


    models = {
        u'player.elo': {
            'Meta': {'object_name': 'Elo'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contestant'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'contestants'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'real_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'start_elo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'waiting_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'player.player': {
            'Meta': {'unique_together': "(('playername', 'birth_date'),)", 'object_name': 'Player'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'coefficientK': ('django.db.models.fields.IntegerField', [], {'default': '10', 'blank': 'True'}),
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

    complete_apps = ['player']