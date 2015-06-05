# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def combine_names(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    for user in CustomUser.objects.all():
        user.full_name = '{} {}'.format(user.first_name, user.last_name)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150605_add_full_name'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
