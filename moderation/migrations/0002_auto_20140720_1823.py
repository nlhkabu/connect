# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistration',
            name='moderator',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserRegistration',
        ),
    ]
