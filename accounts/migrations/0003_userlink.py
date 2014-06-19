# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('anchor', models.CharField(verbose_name='Anchor Text', max_length=100)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Link',
                'unique_together': set([('user', 'url'), ('user', 'anchor')]),
            },
            bases=(models.Model,),
        ),
    ]
