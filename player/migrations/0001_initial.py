# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'player_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('playername', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('rate', self.gf('django.db.models.fields.IntegerField')(default=50, db_index=True, blank=True)),
            ('coefficientK', self.gf('django.db.models.fields.IntegerField')(default=10, blank=True)),
            ('result', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('place', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('degree', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_self_player', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('color_list', self.gf('django.db.models.fields.CharField')(default='w', max_length=4)),
            ('country', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'player', ['Player'])

        # Adding unique constraint on 'Player', fields ['playername', 'birth_date']
        db.create_unique(u'player_player', ['playername', 'birth_date'])

        # Adding model 'Elo'
        db.create_table(u'player_elo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['player.Player'], unique=True)),
            ('waiting_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('real_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('start_elo', self.gf('django.db.models.fields.IntegerField')(default=50, blank=True)),
        ))
        db.send_create_signal(u'player', ['Elo'])

        # Adding M2M table for field contestants on 'Elo'
        m2m_table_name = db.shorten_name(u'player_elo_contestants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('elo', models.ForeignKey(orm[u'player.elo'], null=False)),
            ('player', models.ForeignKey(orm[u'player.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['elo_id', 'player_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Player', fields ['playername', 'birth_date']
        db.delete_unique(u'player_player', ['playername', 'birth_date'])

        # Deleting model 'Player'
        db.delete_table(u'player_player')

        # Deleting model 'Elo'
        db.delete_table(u'player_elo')

        # Removing M2M table for field contestants on 'Elo'
        db.delete_table(db.shorten_name(u'player_elo_contestants'))


    models = {
        u'player.elo': {
            'Meta': {'object_name': 'Elo'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'contestant'", 'blank': 'True', 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['player.Player']", 'unique': 'True'}),
            'real_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'start_elo': ('django.db.models.fields.IntegerField', [], {'default': '50', 'blank': 'True'}),
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