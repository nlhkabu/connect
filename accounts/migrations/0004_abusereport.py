# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_userregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbuseReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('logged_datetime', models.DateTimeField(auto_now_add=True)),
                ('abuse_comment', models.TextField()),
                ('moderator_decision', models.CharField(choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn Abuser'), ('BAN', 'Ban Abuser')], blank=True, max_length=20)),
                ('moderator_comment', models.TextField(blank=True)),
                ('decision_datetime', models.DateTimeField(null=True, blank=True)),
                ('logged_against', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('logged_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('moderator', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'Abuse Report',
            },
            bases=(models.Model,),
        ),
    ]
