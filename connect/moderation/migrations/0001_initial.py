# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationLogMsg',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('msg_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date and time recorded')),
                ('msg_type', models.CharField(max_length=20, verbose_name='message type', choices=[('ALL', 'All'), ('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')])),
                ('comment', models.TextField(verbose_name='log comment')),
                ('logged_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='Moderator who created the log', verbose_name='logged by', related_name='log_messages_by')),
                ('pertains_to', models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='User who moderation log is about', verbose_name='pertains to', related_name='log_messages_about')),
            ],
            options={
                'verbose_name_plural': 'log entries',
                'verbose_name': 'log entry',
            },
            bases=(models.Model,),
        ),
    ]
