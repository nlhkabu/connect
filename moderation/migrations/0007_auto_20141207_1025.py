# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0006_auto_20141104_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moderationlogmsg',
            options={'verbose_name': 'log entry', 'verbose_name_plural': 'log entries'},
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='comment',
            field=models.TextField(verbose_name='log comment'),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='logged_by',
            field=models.ForeignKey(related_name='log_messages_by', to=settings.AUTH_USER_MODEL, verbose_name='logged by', help_text='Moderator who created the log'),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='msg_datetime',
            field=models.DateTimeField(verbose_name='date and time recorded', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='msg_type',
            field=models.CharField(verbose_name='message type', choices=[('ALL', 'All'), ('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')], max_length=20),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='pertains_to',
            field=models.ForeignKey(related_name='log_messages_about', to=settings.AUTH_USER_MODEL, verbose_name='pertains to', help_text='User who moderation log is about'),
        ),
    ]
