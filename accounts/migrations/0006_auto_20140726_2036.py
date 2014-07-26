# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20140721_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistration',
            name='moderator',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserRegistration',
        ),
        migrations.AddField(
            model_name='customuser',
            name='activated_datetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='application_comments',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='applied_datetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='auth_token',
            field=models.CharField(blank=True, verbose_name='Authentication token', max_length=40, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='auth_token_is_used',
            field=models.BooleanField(verbose_name='Token is used', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='decision_datetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='moderator',
            field=models.ForeignKey(null=True, blank=True, help_text='Moderator who invited, approved or rejected this user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='moderator_decision',
            field=models.CharField(choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')], blank=True, max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='registration_method',
            field=models.CharField(choices=[('INV', 'Invited'), ('REQ', 'Requested')], max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
    ]
