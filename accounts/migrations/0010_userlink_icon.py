# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customuser_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlink',
            name='icon',
            field=models.ForeignKey(to='accounts.LinkBrand', blank=True, null=True),
            preserve_default=True,
        ),
    ]
