# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect_config', '0002_auto_20141104_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siteconfig',
            options={'verbose_name': 'site configuration', 'verbose_name_plural': 'site configurations'},
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='email',
            field=models.EmailField(verbose_name='email', max_length=75, help_text='Email for receiving site-wide enquiries'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='email_header',
            field=models.ImageField(verbose_name='email header', upload_to='', help_text='Header image on site generated emails. Must be 600px wide. Keep the file size as small as possible!'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='logo',
            field=models.ImageField(verbose_name='logo', upload_to='', help_text='Must be no larger than 80px by 160px'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='site',
            field=models.OneToOneField(to='sites.Site', related_name='config', verbose_name='site'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='tagline',
            field=models.CharField(verbose_name='site tagline', max_length=200),
        ),
    ]
