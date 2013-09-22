# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Elo.contestant'
        db.delete_column(u'player_elo', 'contestant_id')


        # Changing field 'Elo.player'
        db.alter_column(u'player_elo', 'player_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['player.Player'], unique=True))
        # Adding unique constraint on 'Elo', fields ['player']
        db.create_unique(u'player_elo', ['player_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Elo', fields ['player']
        db.delete_unique(u'player_elo', ['player_id'])

        # Adding field 'Elo.contestant'
        db.add_column(u'player_elo', 'contestant',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='contestant', to=orm['player.Player'], blank=True),
                      keep_default=False)


        # Changing field 'Elo.player'
        db.alter_column(u'player_elo', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player']))

    models = {
        u'player.elo': {
            'Meta': {'object_name': 'Elo'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'contestants'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['player.Player']", 'unique': 'True'}),
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