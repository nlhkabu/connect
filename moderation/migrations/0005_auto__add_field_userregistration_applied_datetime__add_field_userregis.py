# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserRegistration.applied_datetime'
        db.add_column('moderation_userregistration', 'applied_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserRegistration.application_comments'
        db.add_column('moderation_userregistration', 'application_comments',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)


        # Changing field 'UserRegistration.approved_datetime'
        db.alter_column('moderation_userregistration', 'approved_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'UserRegistration.moderator'
        db.alter_column('moderation_userregistration', 'moderator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    def backwards(self, orm):
        # Deleting field 'UserRegistration.applied_datetime'
        db.delete_column('moderation_userregistration', 'applied_datetime')

        # Deleting field 'UserRegistration.application_comments'
        db.delete_column('moderation_userregistration', 'application_comments')


        # Changing field 'UserRegistration.approved_datetime'
        db.alter_column('moderation_userregistration', 'approved_datetime', self.gf('django.db.models.fields.DateTimeField')(default=1))

        # Changing field 'UserRegistration.moderator'
        db.alter_column('moderation_userregistration', 'moderator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], default=datetime.datetime(2014, 3, 6, 0, 0)))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
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
            'msg_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'msg_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pertains_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_messages_about'", 'to': "orm['auth.User']"})
        },
        'moderation.userregistration': {
            'Meta': {'object_name': 'UserRegistration'},
            'application_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applied_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'auth_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'auth_token_is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'related_name': "'inviter'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['moderation']