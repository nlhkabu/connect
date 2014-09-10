# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('logo', models.ImageField(help_text='Must be no larger than 80px by 160px', upload_to='')),
                ('tagline', models.CharField(max_length=200)),
                ('email', models.EmailField(help_text='Email for receiving site-wide enquiries', max_length=75)),
                ('email_header', models.ImageField(help_text='Header image on site generated emails.Must be 600px wide.Keep the file size as small as possible!', upload_to='')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
            bases=(models.Model,),
        ),
    ]
