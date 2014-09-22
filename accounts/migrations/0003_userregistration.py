# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('method', models.CharField(choices=[('INV', 'Invited'), ('REQ', 'Requested')], max_length=20)),
                ('applied_datetime', models.DateTimeField(blank=True, null=True)),
                ('application_comments', models.TextField(blank=True)),
                ('moderator_decision', models.CharField(choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')], blank=True, max_length=20)),
                ('decision_datetime', models.DateTimeField(blank=True, null=True)),
                ('auth_token', models.CharField(verbose_name='Authetication token', blank=True, max_length=40)),
                ('activated_datetime', models.DateTimeField(blank=True, null=True)),
                ('auth_token_is_used', models.BooleanField(verbose_name='Token is used', default=False)),
                ('moderator', models.ForeignKey(help_text='Moderator who invited, approved or rejected this user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Registration',
            },
            bases=(models.Model,),
        ),
    ]
