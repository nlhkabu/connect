# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20141104_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abusereport',
            options={'verbose_name': 'abuse report', 'verbose_name_plural': 'abuse reports'},
        ),
        migrations.AlterModelOptions(
            name='linkbrand',
            options={'verbose_name': 'brand', 'verbose_name_plural': 'brands'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'role', 'verbose_name_plural': 'roles'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'skill', 'verbose_name_plural': 'skills'},
        ),
        migrations.AlterModelOptions(
            name='userlink',
            options={'verbose_name': 'link', 'verbose_name_plural': 'links'},
        ),
        migrations.AlterModelOptions(
            name='userskill',
            options={'verbose_name': 'user skill', 'verbose_name_plural': 'user skills'},
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='abuse_comment',
            field=models.TextField(verbose_name='abuse comment', help_text='Content of abuse report'),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='decision_datetime',
            field=models.DateTimeField(verbose_name='decision datetime', blank=True, help_text='Time and date when moderator made a decision on the report', null=True),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='logged_against',
            field=models.ForeignKey(related_name='abuse_reports_about', to=settings.AUTH_USER_MODEL, verbose_name='logged against', help_text='User who is subject of abuse report'),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='logged_by',
            field=models.ForeignKey(related_name='abuse_reports_by', to=settings.AUTH_USER_MODEL, verbose_name='logged by', help_text='User who logged the abuse report'),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='logged_datetime',
            field=models.DateTimeField(verbose_name='date and time logged', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='moderator',
            field=models.ForeignKey(blank=True, related_name='abuse_reports_moderated_by', to=settings.AUTH_USER_MODEL, verbose_name='moderator', help_text='Moderator who has decided on report', null=True),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='moderator_comment',
            field=models.TextField(verbose_name='moderator comment', blank=True),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='moderator_decision',
            field=models.CharField(verbose_name='moderator decision', blank=True, choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn User'), ('BAN', 'Ban User')], max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activated_datetime',
            field=models.DateTimeField(verbose_name='date account activated', blank=True, help_text='Date and time when user activated their account', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='application_comments',
            field=models.TextField(verbose_name='application comments', blank=True, help_text='Information user supplied when applying for an account (if applicable)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='applied_datetime',
            field=models.DateTimeField(verbose_name='date applied', blank=True, help_text='When user applied for an account (if applicable)', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='auth_token',
            field=models.CharField(verbose_name='authentication token', blank=True, help_text='Token for user to activate their account', max_length=40),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='auth_token_is_used',
            field=models.BooleanField(verbose_name='token is used', default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(verbose_name='biography', blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='decision_datetime',
            field=models.DateTimeField(verbose_name='decision datetime', blank=True, help_text='When moderator made their decision to invite, approve or reject this user', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_moderator',
            field=models.BooleanField(verbose_name='moderator status', default=False, help_text='Designates whether the user has moderator privileges.'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='moderator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='moderator', help_text='Moderator who invited, approved or rejected this user', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='moderator_decision',
            field=models.CharField(verbose_name='moderator decision', blank=True, choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')], max_length=3),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_method',
            field=models.CharField(verbose_name='registration method', choices=[('INV', 'Invited'), ('REQ', 'Requested')], max_length=3),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(verbose_name='role', blank=True, to='accounts.Role', null=True),
        ),
        migrations.AlterField(
            model_name='linkbrand',
            name='domain',
            field=models.CharField(verbose_name='domain', unique=True, help_text='Do not include scheme (e.g. http://, https://)  or subdomain (e.g. www.). Valid examples include "github.com", "facebook.com", etc.', max_length=100),
        ),
        migrations.AlterField(
            model_name='linkbrand',
            name='fa_icon',
            field=models.CharField(verbose_name='font awesome icon', help_text='Choose an icon name from <a href="http://fontawesome.io/icons/">Font Awesome</a> (v4.2.0)', max_length=100),
        ),
        migrations.AlterField(
            model_name='linkbrand',
            name='name',
            field=models.CharField(verbose_name='brand name', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(verbose_name='name', max_length=100),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(verbose_name='name', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='skill',
            name='owner',
            field=models.ManyToManyField(verbose_name='owner', to=settings.AUTH_USER_MODEL, through='accounts.UserSkill'),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='anchor',
            field=models.CharField(verbose_name='anchor text', max_length=100),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='icon',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.LinkBrand', verbose_name='icon', null=True),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='url',
            field=models.URLField(verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='userlink',
            name='user',
            field=models.ForeignKey(related_name='links', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='proficiency',
            field=models.IntegerField(verbose_name='proficiency', choices=[('', '---------'), (10, 'Beginner'), (20, 'Intermediate'), (30, 'Advanced'), (40, 'Expert')], default=10, max_length=2),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='skill',
            field=models.ForeignKey(verbose_name='skill', to='accounts.Skill'),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
