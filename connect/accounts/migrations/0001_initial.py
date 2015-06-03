# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('is_closed', models.BooleanField(verbose_name='closed', help_text='Designates whether the user has closed their own account.', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('bio', models.TextField(verbose_name='biography', blank=True)),
                ('is_moderator', models.BooleanField(verbose_name='moderator status', help_text='Designates whether the user has moderator privileges.', default=False)),
                ('registration_method', models.CharField(verbose_name='registration method', max_length=3, choices=[('INV', 'Invited'), ('REQ', 'Requested')])),
                ('applied_datetime', models.DateTimeField(blank=True, verbose_name='date applied', help_text='When user applied for an account (if applicable)', null=True)),
                ('application_comments', models.TextField(blank=True, verbose_name='application comments', help_text='Information user supplied when applying for an account (if applicable)')),
                ('moderator_decision', models.CharField(blank=True, verbose_name='moderator decision', max_length=3, choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')])),
                ('decision_datetime', models.DateTimeField(blank=True, verbose_name='decision datetime', help_text='When moderator made their decision to invite, approve or reject this user', null=True)),
                ('auth_token', models.CharField(max_length=40, verbose_name='authentication token', help_text='Token for user to activate their account', blank=True)),
                ('auth_token_is_used', models.BooleanField(verbose_name='token is used', default=False)),
                ('activated_datetime', models.DateTimeField(blank=True, verbose_name='date account activated', help_text='Date and time when user activated their account', null=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, related_query_name='user', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set')),
                ('moderator', models.ForeignKey(verbose_name='moderator', blank=True, to=settings.AUTH_USER_MODEL, help_text='Moderator who invited, approved or rejected this user', null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'permissions': (('access_moderators_section', 'Can see the moderators section'), ('invite_user', 'Can issue or reissue an invitation'), ('uninvite_user', 'Can revoke a user invitation'), ('approve_user_application', "Can approve a user's application"), ('reject_user_application', "Can reject a user's application"), ('dismiss_abuse_report', 'Can dismiss an abuse report'), ('warn_user', 'Can warn a user in response to an abuse report'), ('ban_user', 'Can ban a user in response to an abuse report')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbuseReport',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('logged_datetime', models.DateTimeField(verbose_name='date and time logged', default=django.utils.timezone.now)),
                ('abuse_comment', models.TextField(verbose_name='abuse comment', help_text='Content of abuse report')),
                ('moderator_decision', models.CharField(blank=True, verbose_name='moderator decision', max_length=20, choices=[('DISMISS', 'Dismiss Report'), ('WARN', 'Warn User'), ('BAN', 'Ban User')])),
                ('moderator_comment', models.TextField(verbose_name='moderator comment', blank=True)),
                ('decision_datetime', models.DateTimeField(blank=True, verbose_name='decision datetime', help_text='Time and date when moderator made a decision on the report', null=True)),
                ('logged_against', models.ForeignKey(verbose_name='logged against', to=settings.AUTH_USER_MODEL, help_text='User who is subject of abuse report', related_name='abuse_reports_about')),
                ('logged_by', models.ForeignKey(verbose_name='logged by', to=settings.AUTH_USER_MODEL, help_text='User who logged the abuse report', related_name='abuse_reports_by')),
                ('moderator', models.ForeignKey(verbose_name='moderator', blank=True, to=settings.AUTH_USER_MODEL, help_text='Moderator who has decided on report', null=True, related_name='abuse_reports_moderated_by')),
            ],
            options={
                'verbose_name': 'abuse report',
                'verbose_name_plural': 'abuse reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LinkBrand',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='brand name', max_length=100, unique=True)),
                ('domain', models.CharField(max_length=100, verbose_name='domain', help_text='Do not include scheme (e.g. http://, https://)  or subdomain (e.g. www.). Valid examples include "github.com", "facebook.com", etc.', unique=True)),
                ('fa_icon', models.CharField(max_length=100, verbose_name='font awesome icon', help_text='Choose an icon name from <a href="http://fontawesome.io/icons/">Font Awesome</a> (v4.2.0)')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('anchor', models.CharField(verbose_name='anchor text', max_length=100)),
                ('url', models.URLField(verbose_name='url')),
                ('icon', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='icon', blank=True, to='accounts.LinkBrand', null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='links')),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('proficiency', models.IntegerField(verbose_name='proficiency', max_length=2, default=10, choices=[('', '---------'), (10, 'Beginner'), (20, 'Intermediate'), (30, 'Advanced'), (40, 'Expert')])),
                ('skill', models.ForeignKey(verbose_name='skill', to='accounts.Skill')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user skill',
                'verbose_name_plural': 'user skills',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together=set([('user', 'skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='userlink',
            unique_together=set([('user', 'url'), ('user', 'anchor')]),
        ),
        migrations.AddField(
            model_name='skill',
            name='owner',
            field=models.ManyToManyField(through='accounts.UserSkill', verbose_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(verbose_name='role', to='accounts.Role', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', blank=True, related_query_name='user', to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set'),
            preserve_default=True,
        ),
    ]
