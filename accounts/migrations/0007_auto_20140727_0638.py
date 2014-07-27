# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20140726_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activated_datetime',
            field=models.DateTimeField(blank=True, help_text='When user activated their account', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='application_comments',
            field=models.TextField(blank=True, help_text='Information user supplied when applying for an account (if applicable)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='applied_datetime',
            field=models.DateTimeField(blank=True, help_text='When user applied for an account (if applicable)', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='decision_datetime',
            field=models.DateTimeField(blank=True, help_text='When moderator made decision to invite, approve or reject this user', null=True),
        ),
    ]
