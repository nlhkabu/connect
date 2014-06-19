# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.OneToOneField(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True)),
                ('is_moderator', models.BooleanField(default=False)),
                ('connect_preferences', models.ManyToManyField(to='accounts.ConnectPreference', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
