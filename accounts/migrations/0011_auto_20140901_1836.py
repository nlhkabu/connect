# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_userlink_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abusereport',
            name='logged_against',
            field=models.ForeignKey(related_name='abuse_reports_about', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='logged_by',
            field=models.ForeignKey(related_name='abuse_reports_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='moderator',
            field=models.ForeignKey(null=True, blank=True, related_name='abuse_reports_moderated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_name='user_set', verbose_name='groups', to='auth.Group', related_query_name='user'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, related_name='user_set', verbose_name='user permissions', to='auth.Permission', related_query_name='user'),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='icon',
            field=models.ForeignKey(null=True, blank=True, to='accounts.LinkBrand', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='user',
            field=models.ForeignKey(related_name='links', to=settings.AUTH_USER_MODEL),
        ),
    ]
