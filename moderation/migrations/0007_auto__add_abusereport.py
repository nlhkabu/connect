# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AbuseReport'
        db.create_table('moderation_abusereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logged_against', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abuse_reports_about', to=orm['auth.User'])),
            ('logged_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abuse_reports_by', to=orm['auth.User'])),
            ('logged_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('abuse_comment', self.gf('django.db.models.fields.TextField')()),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abuse_reports_moderatored_by', blank=True, to=orm['auth.User'], null=True)),
            ('moderator_decision', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('moderator_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('decision_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
        ))
        db.send_create_signal('moderation', ['AbuseReport'])


    def backwards(self, orm):
        # Deleting model 'AbuseReport'
        db.delete_table('moderation_abusereport')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'moderation.abusereport': {
            'Meta': {'object_name': 'AbuseReport'},
            'abuse_comment': ('django.db.models.fields.TextField', [], {}),
            'decision_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_against': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abuse_reports_about'", 'to': "orm['auth.User']"}),
            'logged_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abuse_reports_by'", 'to': "orm['auth.User']"}),
            'logged_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abuse_reports_moderatored_by'", 'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'moderator_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'moderator_decision': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'moderation.moderationlogmsg': {
            'Meta': {'object_name': 'ModerationLogMsg'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_messages_by'", 'to': "orm['auth.User']"}),
            'msg_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'msg_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pertains_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_messages_about'", 'to': "orm['auth.User']"})
        },
        'moderation.userregistration': {
            'Meta': {'object_name': 'UserRegistration'},
            'activated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'application_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applied_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'auth_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'auth_token_is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'decision_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviter'", 'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'moderator_decision': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['moderation']