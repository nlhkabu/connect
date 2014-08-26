# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0003_auto_20140720_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationlogmsg',
            name='msg_type',
            field=models.CharField(max_length=20, choices=[('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')]),
        ),
    ]
