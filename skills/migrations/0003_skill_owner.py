# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_userskill'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='owner',
            field=models.ManyToManyField(through='skills.UserSkill', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
