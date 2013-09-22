# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Round'
        db.create_table(u'game_round', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('report', self.gf('django.db.models.fields.CharField')(max_length=8192)),
            ('couples', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal(u'game', ['Round'])

        # Adding M2M table for field winners on 'Round'
        m2m_table_name = db.shorten_name(u'game_round_winners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('round', models.ForeignKey(orm[u'game.round'], null=False)),
            ('player', models.ForeignKey(orm[u'player.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['round_id', 'player_id'])

        # Adding M2M table for field draws on 'Round'
        m2m_table_name = db.shorten_name(u'game_round_draws')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('round', models.ForeignKey(orm[u'game.round'], null=False)),
            ('player', models.ForeignKey(orm[u'player.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['round_id', 'player_id'])

        # Adding M2M table for field losers on 'Round'
        m2m_table_name = db.shorten_name(u'game_round_losers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('round', models.ForeignKey(orm[u'game.round'], null=False)),
            ('player', models.ForeignKey(orm[u'player.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['round_id', 'player_id'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Round'])),
            ('black_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='black_player', to=orm['player.Player'])),
            ('white_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='white_player', to=orm['player.Player'])),
            ('result', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('btime_limit', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('wtime_limit', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('steps', self.gf('django.db.models.fields.TextField')(default='', max_length=8196, blank=True)),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'Total'
        db.create_table(u'game_total', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('time_rule', self.gf('django.db.models.fields.TextField')(default='', max_length=1024, blank=True)),
            ('category', self.gf('django.db.models.fields.TextField')(default='', max_length=1024, blank=True)),
            ('addition_coefficients', self.gf('django.db.models.fields.TextField')(default='', max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'game', ['Total'])

        # Adding M2M table for field players on 'Total'
        m2m_table_name = db.shorten_name(u'game_total_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('total', models.ForeignKey(orm[u'game.total'], null=False)),
            ('player', models.ForeignKey(orm[u'player.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['total_id', 'player_id'])

        # Adding M2M table for field rounds on 'Total'
        m2m_table_name = db.shorten_name(u'game_total_rounds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('total', models.ForeignKey(orm[u'game.total'], null=False)),
            ('round', models.ForeignKey(orm[u'game.round'], null=False))
        ))
        db.create_unique(m2m_table_name, ['total_id', 'round_id'])


    def backwards(self, orm):
        # Deleting model 'Round'
        db.delete_table(u'game_round')

        # Removing M2M table for field winners on 'Round'
        db.delete_table(db.shorten_name(u'game_round_winners'))

        # Removing M2M table for field draws on 'Round'
        db.delete_table(db.shorten_name(u'game_round_draws'))

        # Removing M2M table for field losers on 'Round'
        db.delete_table(db.shorten_name(u'game_round_losers'))

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'Total'
        db.delete_table(u'game_total')

        # Removing M2M table for field players on 'Total'
        db.delete_table(db.shorten_name(u'game_total_players'))

        # Removing M2M table for field rounds on 'Total'
        db.delete_table(db.shorten_name(u'game_total_rounds'))


    models = {
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'black_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black_player'", 'to': u"orm['player.Player']"}),
            'btime_limit': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Round']"}),
            'steps': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '8196', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'white_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'white_player'", 'to': u"orm['player.Player']"}),
            'wtime_limit': ('django.db.models.fields.TimeField', [], {'blank': 'True'})
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'winners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'winner'", 'blank': 'True', 'to': u"orm['player.Player']"})
        },
        u'game.total': {
            'Meta': {'object_name': 'Total'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'addition_coefficients': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'category': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['player.Player']", 'symmetrical': 'False', 'blank': 'True'}),
            'rounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.Round']", 'symmetrical': 'False', 'blank': 'True'}),
            'time_rule': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
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

    complete_apps = ['game']