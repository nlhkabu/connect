# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbuseReport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('logged_datetime', models.DateTimeField(auto_now_add=True)),
                ('abuse_comment', models.TextField()),
                ('moderator_decision', models.CharField(max_length=20, blank=True, choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn Abuser'), ('BAN', 'Ban Abuser')])),
                ('moderator_comment', models.TextField(blank=True)),
                ('decision_datetime', models.DateTimeField(blank=True, null=True)),
                ('logged_against', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('logged_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('moderator', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Abuse Report',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModerationLogMsg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('msg_datetime', models.DateTimeField(auto_now_add=True)),
                ('msg_type', models.CharField(max_length=20, choices=[('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('REVOCATION', 'Invitation Revoked'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')])),
                ('comment', models.TextField()),
                ('logged_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('pertains_to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Log Entries',
                'verbose_name': 'Log Entry',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('method', models.CharField(max_length=20, choices=[('INV', 'Invited'), ('REQ', 'Requested')])),
                ('applied_datetime', models.DateTimeField(blank=True, null=True)),
                ('application_comments', models.TextField(blank=True)),
                ('moderator_decision', models.CharField(max_length=20, blank=True, choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')])),
                ('decision_datetime', models.DateTimeField(blank=True, null=True)),
                ('auth_token', models.CharField(max_length=40, blank=True, verbose_name='Authetication token')),
                ('activated_datetime', models.DateTimeField(blank=True, null=True)),
                ('auth_token_is_used', models.BooleanField(default=False, verbose_name='Token is used')),
                ('moderator', models.ForeignKey(null=True, help_text='Moderator who invited, approved or rejected this user', blank=True, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Registration',
            },
            bases=(models.Model,),
        ),
    ]
