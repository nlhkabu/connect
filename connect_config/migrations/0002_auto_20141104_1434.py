# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect_config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='site',
            field=models.OneToOneField(to='sites.Site', related_name='config'),
        ),
    ]
