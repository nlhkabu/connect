# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20140901_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abusereport',
            name='logged_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
