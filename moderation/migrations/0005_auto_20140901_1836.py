# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0004_auto_20140826_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='logged_by',
            field=models.ForeignKey(related_name='log_messages_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='msg_type',
            field=models.CharField(choices=[('ALL', 'All'), ('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')], max_length=20),
        ),
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='pertains_to',
            field=models.ForeignKey(related_name='log_messages_about', to=settings.AUTH_USER_MODEL),
        ),
    ]
