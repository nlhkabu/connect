# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0002_auto_20140720_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abusereport',
            name='logged_against',
        ),
        migrations.RemoveField(
            model_name='abusereport',
            name='logged_by',
        ),
        migrations.RemoveField(
            model_name='abusereport',
            name='moderator',
        ),
        migrations.DeleteModel(
            name='AbuseReport',
        ),
    ]
