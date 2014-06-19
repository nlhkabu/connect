# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectPreference',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Preference',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LinkBrand',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('fa_icon', models.CharField(verbose_name='Font Awesome Icon', max_length=100, help_text='Choose an icon name from <a href="http://fontawesome.io/icons/">Font Awesome</a> (v4.0.3)')),
            ],
            options={
                'verbose_name': 'Brand',
            },
            bases=(models.Model,),
        ),
    ]
