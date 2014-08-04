# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20140727_0638'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConnectPreference',
            new_name='Role',
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Role'},
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='connect_preferences',
            new_name='roles',
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='moderator_decision',
            field=models.CharField(blank=True, choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn User'), ('BAN', 'Ban User')], max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='moderator_decision',
            field=models.CharField(blank=True, choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')], max_length=3),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_method',
            field=models.CharField(choices=[('INV', 'Invited'), ('REQ', 'Requested')], max_length=3),
        ),
        migrations.AlterField(
            model_name='linkbrand',
            name='domain',
            field=models.CharField(unique=True, max_length=100, help_text='Do not include scheme (e.g. http://, https://)  or subdomain (e.g. www.) e.g github.com, facebook.com, etc.'),
        ),
    ]
