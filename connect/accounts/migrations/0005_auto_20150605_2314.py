# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150605_remove_first_name_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(verbose_name='role', to='accounts.Role', blank=True),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='proficiency',
            field=models.IntegerField(verbose_name='proficiency', choices=[('', '---------'), (10, 'Beginner'), (20, 'Intermediate'), (30, 'Advanced'), (40, 'Expert')], default=10),
        ),
    ]
