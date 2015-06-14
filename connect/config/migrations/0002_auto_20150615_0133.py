# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='email',
            field=models.EmailField(verbose_name='email', max_length=254, help_text='Email for receiving site-wide enquiries'),
        ),
    ]
