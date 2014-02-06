# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ConnectPreferences'
        db.delete_table('profiles_connectpreferences')

        # Deleting model 'Profile'
        db.delete_table('profiles_profile')

        # Removing M2M table for field connect_preferences on 'Profile'
        db.delete_table(db.shorten_name('profiles_profile_connect_preferences'))


    def backwards(self, orm):
        # Adding model 'ConnectPreferences'
        db.create_table('profiles_connectpreferences', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('profiles', ['ConnectPreferences'])

        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(blank=True, max_length=100)),
        ))
        db.send_create_signal('profiles', ['Profile'])

        # Adding M2M table for field connect_preferences on 'Profile'
        m2m_table_name = db.shorten_name('profiles_profile_connect_preferences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['profiles.profile'], null=False)),
            ('connectpreferences', models.ForeignKey(orm['profiles.connectpreferences'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'connectpreferences_id'])


    models = {
        
    }

    complete_apps = ['profiles']