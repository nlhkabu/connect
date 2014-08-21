# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20140804_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_closed',
            field=models.BooleanField(help_text='Designates whether the user has closed their own account.', default=False, verbose_name='closed'),
            preserve_default=True,
        ),
    ]
