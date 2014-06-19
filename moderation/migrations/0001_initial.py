# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbuseReport',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('logged_against', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('logged_by', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('logged_datetime', models.DateTimeField(auto_now_add=True)),
                ('abuse_comment', models.TextField()),
                ('moderator', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, to_field='id')),
                ('moderator_decision', models.CharField(choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn Abuser'), ('BAN', 'Ban Abuser')], max_length=20, blank=True)),
                ('moderator_comment', models.TextField(blank=True)),
                ('decision_datetime', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Abuse Report',
            },
            bases=(models.Model,),
        ),
    ]
