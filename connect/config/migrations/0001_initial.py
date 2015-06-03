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
                ('logo', models.ImageField(help_text='Must be no larger than 80px by 160px', verbose_name='logo', upload_to='')),
                ('tagline', models.CharField(verbose_name='site tagline', max_length=200)),
                ('email', models.EmailField(help_text='Email for receiving site-wide enquiries', verbose_name='email', max_length=75)),
                ('email_header', models.ImageField(help_text='Header image on site generated emails. Must be 600px wide. Keep the file size as small as possible!', verbose_name='email header', upload_to='')),
                ('site', models.OneToOneField(related_name='config', to='sites.Site', verbose_name='site')),
            ],
            options={
                'verbose_name_plural': 'site configurations',
                'verbose_name': 'site configuration',
            },
            bases=(models.Model,),
        ),
    ]
