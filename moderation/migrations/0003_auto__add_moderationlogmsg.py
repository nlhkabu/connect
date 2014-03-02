# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModerationLogMsg'
        db.create_table('moderation_moderationlogmsg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msg_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('msg_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('pertains_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='log_messages_about', to=orm['auth.User'])),
            ('logged_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='log_messages_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('moderation', ['ModerationLogMsg'])


    def backwards(self, orm):
        # Deleting model 'ModerationLogMsg'
        db.delete_table('moderation_moderationlogmsg')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'moderation.moderationlogmsg': {
            'Meta': {'object_name': 'ModerationLogMsg'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_messages_by'", 'to': "orm['auth.User']"}),
            'msg_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'msg_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pertains_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_messages_about'", 'to': "orm['auth.User']"})
        },
        'moderation.userregistration': {
            'Meta': {'object_name': 'UserRegistration'},
            'approved_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'auth_token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'auth_token_is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviter'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['moderation']